# aws-team-cost-aggregator
Companion tool to the [AWS Team Cost Reporter](https://github.com/Signiant/aws-team-cost-reporter). Generates a summary for all teams in one email report

# Purpose
The AWS Team cost reporter tool generates individual emails to report each team's cost but it's helpful to have an aggregate summary as well. That is the purpose of this tool - read the output data from the cost reporter and generate a summary email.

# Sample Report Email

The email report that gets generated for the summary looks something like this...

![Sample Report](https://raw.githubusercontent.com/Signiant/aws-team-cost-aggregator/master/images/sample-email.jpg)

# Prerequisites
* You should have run the cost reporter tool and have the raw results data in a folder somewhere.  See that tools docs on how to bind mount a volume for the results data.
* You'll need a config file created for the tool.  See the samples folder for a small sample config file

# Usage

The easiest way to run the tool is from docker (because docker rocks).  You just pass it a folder containing the raw results files and a config file and it will do everything from there

```bash
docker pull signiant/aws-team-cost-aggregator
```

```bash
docker run \
   -v /config/myconfigfile.yaml:/config.yaml \
   -v /local/results-folder:/results:rw \
   signiant/aws-team-cost-aggregator \
        -c /config.yaml \
        -f /results \
        -r
```

In this example, we use a bindmount to mount in the config file from a local folder to the root directory of the container.  We can then pass the -c argument to the container to have it read the config from / and use the team name of team-one.

We also use a bind mount to mount in the results folder so the tool in the container can read it.  In this case we mount it in read write so we can remove the results files when we are done (the -r flag)

There is an optional -d flag to the tool which will turn on more debug output.  For example:

```bash
docker run \
   -v /config/myconfigfile.yaml:/config.yaml \
   -v /local/results-folder:/results:rw \
   signiant/aws-team-cost-aggregator \
        -c /config.yaml \
        -f /results \
        -r \
        -d
```
