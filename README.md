[![Circle CI](https://circleci.com/gh/rackspace-orchestration-templates/graphite/tree/master.png?style=shield)](https://circleci.com/gh/rackspace-orchestration-templates/graphite)
Description
===========

This is a template for deploying a single Linux server running
[Graphite](http://graphite.readthedocs.org) and
[Statsd](https://github.com/etsy/statsd/).

Requirements
============
* A Heat provider that supports the Rackspace `OS::Heat::ChefSolo` plugin.
* An OpenStack username, password, and tenant id.
* [python-heatclient](https://github.com/openstack/python-heatclient)
`>= v0.2.8`:

```bash
pip install python-heatclient
```

We recommend installing the client within a [Python virtual
environment](http://www.virtualenv.org/).

Example Usage
=============
Here is an example of how to deploy this template using the
[python-heatclient](https://github.com/openstack/python-heatclient):

```
heat --os-username <OS-USERNAME> --os-password <OS-PASSWORD> --os-tenant-id \
  <TENANT-ID> --os-auth-url https://identity.api.rackspacecloud.com/v2.0/ \
  stack-create Graphite-Stack -f graphite.yaml \
  -P flavor="4 GB Performance"
```

* For UK customers, use `https://lon.identity.api.rackspacecloud.com/v2.0/` as
the `--os-auth-url`.

Optionally, set environmental variables to avoid needing to provide these
values every time a call is made:

```
export OS_USERNAME=<USERNAME>
export OS_PASSWORD=<PASSWORD>
export OS_TENANT_ID=<TENANT-ID>
export OS_AUTH_URL=<AUTH-URL>
```

Parameters
==========
Parameters can be replaced with your own values when standing up a stack. Use
the `-P` flag to specify a custom parameter.

* `image`: Operating system to install (Default: Ubuntu 12.04 LTS (Precise
  Pangolin))
* `flavor`: Cloud server size to use. (Default: 2 GB Performance)
* `kitchen`: URL for the kitchen to clone with git. The Chef Solo run will copy
  all files in this repo into the kitchen for the chef run. (Default:
  https://github.com/rackspace-orchestration-templates/graphite)
* `chef_version`: Chef client version to install for the chef run.  (Default:
  11.12.8)

Outputs
=======
Once a stack comes online, use `heat output-list` to see all available outputs.
Use `heat output-show <OUTPUT NAME>` to get the value fo a specific output.

* `private_key`: SSH private that can be used to login as root to the server.
* `server_ip`: Public IP address of the cloud server
* `graphite_password`: Password to use when logging into Graphite as `root`
* `graphite_url`: URL to use when navigating to the Graphite installation

For multi-line values, the response will come in an escaped form. To get rid of
the escapes, use `echo -e '<STRING>' > file.txt`. For vim users, a substitution
can be done within a file using `%s/\\n/\r/g`.

Stack Details
=============
#### Getting Started
If you are new to Graphite the [Graphite
Overview](http://graphite.readthedocs.org/en/latest/overview.html) page
provides a good description of what Graphite is and what it is not. A good
writeup on
[StatsD](http://codeascraft.com/2011/02/15/measure-anything-measure-everything/)
is provided by the guys that wrote it.

#### Accessing Your Deployment
Navigate to the IP of the server you've created in a browser. Use the login of
`root` and the `graphite_password` provided in the outputs section.

#### Logging In via SSH
The private key provided in the passwords section can be used to login as root
via SSH. We have an article on how to use these keys with [Mac OS X and
Linux](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-linuxmac)
as well as [Windows using
PuTTY](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-windows).

#### Details of Your Setup
The deployment was stood up using
[chef-solo](http://docs.opscode.com/chef_solo.html). Once the deployment is up,
chef will not run again, so it is safe to modify configurations.

The Graphite Webapp runs under Apache as WSGI module on the standard HTTP TCP
port of 80. The webapp provides the graphing UI, a simple dashboard, as well as
an API to get stored metrics out. It draws graphs with times in the UTC
timezone. You can change the timezone by modifying the
/opt/graphite/webapp/graphite/local_settings.py file and restarting Apache. You
can login to the Webapp using the user `root` and the `graphite_password`
supplied in the outputs section.

Carbon is a Graphite backend server process that accepts time-series data on
TCP port 2003. Carbon can be configured via the /opt/graphite/conf/carbon.conf
file. Carbon uses Whisper to store the data on disk which is configured to
store data at 1 minute intervals for 3 months and after three months the data
is averaged into 5 minute intervals for 2 years. The default storage schema can
be changed or added to in the /opt/graphite/conf/storage-schema.conf file.

[Statsd](https://github.com/etsy/statsd/) is a network daemon that sits along
side Graphite also listening for metrics to be written to it on UDP port 8125.
It writes its aggregated metrics to the local Graphite Carbon backend. It's
configuration can be customized in the /etc/statsd/config.js file.

Contributing
============
There are substantial changes still happening within the [OpenStack
Heat](https://wiki.openstack.org/wiki/Heat) project. Template contribution
guidelines will be drafted in the near future.

License
=======
```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
