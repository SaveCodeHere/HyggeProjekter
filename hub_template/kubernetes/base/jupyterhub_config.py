import os
from jupyterhub.auth import LDAPAuthenticator
from kubespawner import KubeSpawner
from tornado import gen

# ToDo: Update the LDAP server address, DN templates, search bases, and storage class name

# Replace ldap.company.com with your actual LDAP server
# Update the LDAP DN templates and search bases to match your organization
# Store sensitive information (like lookup_dn_search_password) in secrets
# Adjust the storage class name to match your OpenShift cluster's available storage classes

# c cab be unknown in the "c." jupyterhub will pick up on it
# Basic JupyterHub Configuration
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8888
c.JupyterHub.hub_ip = '0.0.0.0'

# LDAP Authentication Configuration
c.JupyterHub.authenticator_class = LDAPAuthenticator
c.LDAPAuthenticator.server_address = 'ldap.company.com'
c.LDAPAuthenticator.server_port = 389
c.LDAPAuthenticator.use_ssl = True
c.LDAPAuthenticator.bind_dn_template = [
    'uid={username},ou=People,dc=company,dc=com'
]
c.LDAPAuthenticator.lookup_dn = True
c.LDAPAuthenticator.lookup_dn_search_filter = '(&(objectClass=posixAccount)(uid={username}))'
c.LDAPAuthenticator.lookup_dn_search_user = 'cn=admin,dc=company,dc=com'
c.LDAPAuthenticator.lookup_dn_search_password = 'lookup_password'  # Store this securely
c.LDAPAuthenticator.user_search_base = 'ou=People,dc=company,dc=com'
c.LDAPAuthenticator.user_attribute = 'uid'
c.LDAPAuthenticator.allowed_groups = ['jupyter-users']

# OpenShift/Kubernetes Spawner Configuration
c.JupyterHub.spawner_class = KubeSpawner

# Pod configuration
c.KubeSpawner.namespace = 'jupyterhub'
c.KubeSpawner.enable_user_namespaces = True
c.KubeSpawner.user_namespace_template = 'jupyter-user-{username}'

# Container image configuration
c.KubeSpawner.image = 'jupyter/base-notebook:latest'
c.KubeSpawner.image_pull_policy = 'Always'

# Resource limits
c.KubeSpawner.cpu_limit = 1
c.KubeSpawner.cpu_guarantee = 0.1
c.KubeSpawner.mem_limit = '1G'
c.KubeSpawner.mem_guarantee = '512M'

# Pod security context
c.KubeSpawner.service_account = 'jupyterhub-nb'
c.KubeSpawner.run_as_uid = 1000
c.KubeSpawner.fs_gid = 100

# Volume mounts for user data persistence
c.KubeSpawner.user_storage_pvc_ensure = True
c.KubeSpawner.pvc_name_template = 'claim-{username}'
c.KubeSpawner.storage_class = 'standard'
c.KubeSpawner.storage_capacity = '10Gi'

c.KubeSpawner.volumes = [
    {
        'name': 'user-vol',
        'persistentVolumeClaim': {
            'claimName': 'claim-{username}'
        }
    }
]

c.KubeSpawner.volume_mounts = [
    {
        'name': 'user-vol',
        'mountPath': '/home/jovyan/work'
    }
]

# Pod environment configuration
c.KubeSpawner.environment = {
    'JUPYTER_ENABLE_LAB': 'true'
}

# Extra pod labels
c.KubeSpawner.extra_labels = {
    'app': 'jupyterhub',
    'component': 'singleuser-server',
    'hub.jupyter.org/username': '{username}'
}

# Idle server settings
c.JupyterHub.last_activity_interval = 300
c.JupyterHub.admin_access = True

# SSL/TLS Configuration (if needed)
# c.JupyterHub.ssl_key = '/etc/jupyterhub/ssl/ssl.key'
# c.JupyterHub.ssl_cert = '/etc/jupyterhub/ssl/ssl.cert'