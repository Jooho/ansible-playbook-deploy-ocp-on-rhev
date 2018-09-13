#!/usr/bin/env python

import click
import os
import sys
from StringIO import StringIO

@click.command()
@click.option('--provider',
              default='rhev',
              type=click.Choice(['rhev']),
              help='This option specifies provider platform. ',
              show_default=True)
@click.option('--deploy_type',
              default='ocp',
              type=click.Choice(['nfs','ansible-controller', 'ocp', 'scale', 'bg_upgrade', 'logging', 'metrics', 'prometheus','cfme', 'service-catalog' ]),
              help='This option specifies main commands : deploying a new cluster, scaling up/down nodes, blue green upgrade',
              show_default=True)
@click.option('--operate',
              default='deploy',
              type=click.Choice(['create', 'config', 'deploy', 'install', 'undeploy', 'start', 'stop', 'teardown', 'up', 'down', 'warmup', 'upgrade']),
              help='This option specifies sub commands : deploying a new cluster, start/stop/teardown VMs, scaling up/down')
@click.option('--tag',
              help='The tag of cluster used for targeting specific cluster operated to. It will overwrite the value from vars/all ')
@click.option('--target_node_filter',
              help='The filter for VMs in the cluster tag')
@click.option('--ocp_version',
              help='openshift verion. Basically, it will come from vars/all file but it can be overwritten ')
@click.option('--ocp_install',
              is_flag=False,
              help='Adding this flag will delete VM without cordon/drain tasks. This flag is useful for teardown of cluster')
@click.option('--target',
              type=click.Choice(['app', 'infra', 'master', 'node']),
              help='Target node: app/infra for scale, master/node for bg upgrade')
@click.option('--new_cluster_color',
              type=click.Choice(['green', 'blue', None]),
              default=None,
              help='When error happen during bg upgrade, color can be overwritten not to create new nodes.')
@click.option('--instances',
              default='1',
              help='Specifying how many vms will be scaling up/down')
@click.help_option('--help', '-h')
@click.option('-v', '--verbose', count=True)
def launch(provider=None,
           deploy_type=None,
           operate=None,
           tag=None,
           target_node_filter=None,
           ocp_version=None,
           target=None,
           instances=None,
           ocp_install=None,
           new_cluster_color=None,
           verbose=0):

    # validate ansible-controller deploy_type options
    if deploy_type == 'ansible-controller':
        if operate not in ['create', 'config']:
            print "[Not Valid Operate] - '%s' only allowed for ocp" %operate
            sys.exit(1)

    # validate ocp deploy_type options
    if deploy_type == 'ocp':
        if target is not None:
            print "[Not Valid Options] - --target option is for scale/bg_upgrade"
            sys.exit(1)

        if operate not in ['deploy', 'start', 'stop', 'teardown','install']:
            print "[Not Valid Operate] - '%s' only allowed for ocp" %operate
            sys.exit(1)

    # validate scale deploy_type options
    if deploy_type == 'scale':
        if target is None:
            print "[Not Valid Options] - --target_node_filter option is for ocp"
            sys.exit(1)

        if operate not in ['up', 'down']:
            print "[Not Valid Options] - (up/down) only allowed for scale deploy_type"
            sys.exit(1)

    # validate bg_upgrade deploy_type options
    if deploy_type == 'bg_upgrade':
        if target is None:
            print "[Not Valid Options] - target option is essential for bg_upgrade"
            sys.exit(1)

        if operate not in ['deploy', 'warmup']:
            print "[Not Valid Options] - (deploy/warmup) only allowed for bg_upgrade deploy_type"
            sys.exit(1)

    # validate bg_upgrade deploy_type options
    if deploy_type == 'ansible_controller':
        if target_node_filter is not None:
            print "[Not Valid Options] - --target_node_filter option is for ocp"
            sys.exit(1)

        if instances is not None:
            print "[Not Valid Options] - --instances option is for scale"
            sys.exit(1)

        if operate is not None:
            print "[Not Valid Options] - operate is not allowed"
            sys.exit(1)

        if target is not None:
            print "[Not Valid Options] - --target option is for scale/bg_upgrade"
            sys.exit(1)


    if verbose > 0:
        verbosity = '-' + 'v' * verbose
    else:
        verbosity = ''



    # Create variable list to overwrite
    all_variables_str= ["provider", "j_deploy_type", "operate", "tag", "target_node_filter", "ocp_install", "target", "instances", "ocp_version", "new_cluster_color"];
    all_variables_real= [provider, deploy_type, operate, tag, target_node_filter, ocp_install, target, instances, ocp_version, new_cluster_color];
    overwrite_variables=[];
    var_index=0
    sio=StringIO();
    for variable in all_variables_real:
        if variable is not None:
            real_value=str(variable);
            add_value=all_variables_str[var_index]+"="+real_value;
            overwrite_variables.append(add_value);
          #  overwrite_variables.append(add_value);
          #  ''.join(overwrite_variables)
          #  print overwrite_variables;

        var_index += 1

    sio.write(' '.join(overwrite_variables));
    print sio.getvalue();




# Construct ansible command
    if deploy_type == 'ansible-controller' and operate == 'create':
        status = os.system(
             'ansible-playbook %s playbooks/%s/ansible-controller/ansible-controller.yaml \
             --extra-vars "@vars/all" \
             --extra-vars "@vars/ocp_params" \
             -e "%s" '
             % (verbosity, provider, sio.getvalue())
        )
 
    elif deploy_type == 'ansible-controller' and operate == 'config':
        status = os.system(
             'ansible-playbook %s playbooks/%s/ansible-controller/ansible-controller-configure.yaml \
             --extra-vars "@vars/all" \
             --extra-vars "@vars/ocp_params" \
             -e "%s" '
             % (verbosity, provider, sio.getvalue())
        )
 
    elif deploy_type == 'nfs':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/nfs.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e "%s" '

            % (verbosity, sio.getvalue())
              
        )
    
    elif deploy_type == 'metrics' and operate == 'deploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/metrics.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e openshift_metrics_install_metrics=true \
            -e "%s" --tags=always,"%s" '

            % (verbosity, sio.getvalue(), operate)
              
        )

    elif deploy_type == 'metrics' and operate == 'undeploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/metrics.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e openshift_metrics_install_metrics=false \
            -e "%s" --tags=always,"%s" '

            % (verbosity, sio.getvalue(), operate)
              
        )

    elif deploy_type == 'prometheus' and operate == 'deploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/prometheus.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e openshift_hosted_prometheus_deploy=true \
            -e "%s" '

            % (verbosity, sio.getvalue())
              
        )

    elif deploy_type == 'prometheus' and operate == 'undeploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/prometheus.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e openshift_prometheus_state=absent \
            -e "%s" '

            % (verbosity, sio.getvalue())
              
        )

    elif deploy_type == 'cfme' and operate == 'deploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/cfme.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e "%s" '

            % (verbosity, sio.getvalue())
              
        )

    elif deploy_type == 'service-catalog' and operate == 'deploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/service-catalog.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e "%s" '

            % (verbosity, sio.getvalue())
              
        )

    elif deploy_type == 'service-catalog' and operate == 'undeploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/service-catalog.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e openshift_enable_service_catalog=false \
            -e "%s" '

            % (verbosity, sio.getvalue())
              
        )



    elif deploy_type == 'logging' and operate == 'deploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/logging.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e "%s" --tags=always,"%s" '

            % (verbosity, sio.getvalue(), operate)
              
        )
    
    elif deploy_type == 'logging' and operate == 'undeploy':
        status = os.system(
            'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/common/logging.yaml \
            --extra-vars "@vars/all" \
            --extra-vars "@vars/ocp_params" \
            -e openshift_logging_install_logging=false \
            -e "%s" --tags=always,"%s" '

            % (verbosity, sio.getvalue(), operate)
              
        )

    elif deploy_type == 'ocp' and operate == 'install' :
        status = os.system(
             'ansible-playbook %s -i /etc/ansible/hosts playbooks/%s/ocp/ocp-install.yaml \
             --extra-vars "@vars/all" '

             % (verbosity, provider)
        )
 

   
    else:
        if deploy_type != 'prometheus' and deploy_type != 'logging' and deploy_type != 'metrics' and  operate != 'install':
            status = os.system(
                'DEFAULT_KEEP_REMOTE_FILES=yes  ansible-playbook %s playbooks/config.yaml \
                --extra-vars "@vars/all" \
                --extra-vars "@vars/ocp_params" \
                -e "%s" --tags always,"%s"'
 
                % (verbosity, sio.getvalue(),deploy_type)
                  
            )


    # Exit appropriately
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
        sys.exit(os.WEXITSTATUS(status))


if __name__ == '__main__':
    launch(auto_envvar_prefix='RHEV_OCP_DEPLOY')
