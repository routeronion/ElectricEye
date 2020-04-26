# This file is part of ElectricEye.

# ElectricEye is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ElectricEye is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with ElectricEye.  
# If not, see https://github.com/jonrau1/ElectricEye/blob/master/LICENSE.

import boto3
import os
import datetime
# import boto3 clients
sts = boto3.client('sts')
eks = boto3.client('eks')
securityhub = boto3.client('securityhub')
# create region & account variables
awsAccountId = sts.get_caller_identity()['Account']
awsRegion = os.environ['AWS_REGION']

def eks_public_endpoint_access_check():
    # loop through EKS clusters
    response = eks.list_clusters(maxResults=100)
    myEksClusters = response['clusters']
    for clusters in myEksClusters:
        cluster = str(clusters)
        try:
            response = eks.describe_cluster(name=cluster)
            clusterName = str(response['cluster']['name'])
            clusterArn = str(response['cluster']['arn'])
            eksPublicAccessCheck = str(response['cluster']['resourcesVpcConfig']['endpointPublicAccess'])
            if eksPublicAccessCheck == 'True':
                try:
                    # ISO Time
                    iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                    # create Sec Hub finding
                    response = securityhub.batch_import_findings(
                        Findings=[
                            {
                                'SchemaVersion': '2018-10-08',
                                'Id': clusterArn + '/public-endpoint-access-check',
                                'ProductArn': 'arn:aws-us-gov:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                                'GeneratorId': clusterName,
                                'AwsAccountId': awsAccountId,
                                'Types': [
                                    'Software and Configuration Checks/AWS Security Best Practices',
                                    'Effects/Data Exposure'
                                ],
                                'FirstObservedAt': iso8601Time,
                                'CreatedAt': iso8601Time,
                                'UpdatedAt': iso8601Time,
                                'Severity': { 'Label': 'CRITICAL' },
                                'Confidence': 99,
                                'Title': '[EKS.1] Elastic Kubernetes Service (EKS) cluster API servers should not be accessible from the internet',
                                'Description': 'Elastic Kubernetes Service (EKS) cluster ' + clusterName + ' API server is accessible from the internet. Refer to the remediation instructions if this configuration is not intended',
                                'Remediation': {
                                    'Recommendation': {
                                        'Text': 'If your EKS cluster is not intended to be public refer to the Amazon EKS Cluster Endpoint Access Control section of the EKS user guide',
                                        'Url': 'https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html'
                                    }
                                },
                                'ProductFields': {
                                    'Product Name': 'ElectricEye'
                                },
                                'Resources': [
                                    {
                                        'Type': 'AwsEksCluster',
                                        'Id': clusterArn,
                                        'Partition': 'aws-us-gov',
                                        'Region': awsRegion,
                                        'Details': {
                                            'Other': { 'Cluster Name': clusterName }
                                        }
                                    }
                                ],
                                'Compliance': { 
                                    'Status': 'FAILED',
                                    'RelatedRequirements': [
                                        'NIST CSF PR.AC-3',
                                        'NIST SP 800-53 AC-1',
                                        'NIST SP 800-53 AC-17',
                                        'NIST SP 800-53 AC-19',
                                        'NIST SP 800-53 AC-20',
                                        'NIST SP 800-53 SC-15',
                                        'AICPA TSC CC6.6',
                                        'ISO 27001:2013 A.6.2.1',
                                        'ISO 27001:2013 A.6.2.2',
                                        'ISO 27001:2013 A.11.2.6',
                                        'ISO 27001:2013 A.13.1.1',
                                        'ISO 27001:2013 A.13.2.1'
                                    ]
                                },
                                'Workflow': {
                                    'Status': 'NEW'
                                },
                                'RecordState': 'ACTIVE'
                            }
                        ]
                    )
                    print(response)
                except Exception as e:
                    print(e)
            else:
                try:
                    # ISO Time
                    iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                    # create Sec Hub finding
                    response = securityhub.batch_import_findings(
                        Findings=[
                            {
                                'SchemaVersion': '2018-10-08',
                                'Id': clusterArn + '/public-endpoint-access-check',
                                'ProductArn': 'arn:aws-us-gov:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                                'GeneratorId': clusterName,
                                'AwsAccountId': awsAccountId,
                                'Types': [
                                    'Software and Configuration Checks/AWS Security Best Practices',
                                    'Effects/Data Exposure'
                                ],
                                'FirstObservedAt': iso8601Time,
                                'CreatedAt': iso8601Time,
                                'UpdatedAt': iso8601Time,
                                'Severity': { 'Label': 'INFORMATIONAL' },
                                'Confidence': 99,
                                'Title': '[EKS.1] Elastic Kubernetes Service (EKS) cluster API servers should not be accessible from the internet',
                                'Description': 'Elastic Kubernetes Service (EKS) cluster ' + clusterName + ' API server is not accessible from the internet.',
                                'Remediation': {
                                    'Recommendation': {
                                        'Text': 'If your EKS cluster is not intended to be public refer to the Amazon EKS Cluster Endpoint Access Control section of the EKS user guide',
                                        'Url': 'https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html'
                                    }
                                },
                                'ProductFields': {
                                    'Product Name': 'ElectricEye'
                                },
                                'Resources': [
                                    {
                                        'Type': 'AwsEksCluster',
                                        'Id': clusterArn,
                                        'Partition': 'aws-us-gov',
                                        'Region': awsRegion,
                                        'Details': {
                                            'Other': { 'Cluster Name': clusterName }
                                        }
                                    }
                                ],
                                'Compliance': { 
                                    'Status': 'PASSED',
                                    'RelatedRequirements': [
                                        'NIST CSF PR.AC-3',
                                        'NIST SP 800-53 AC-1',
                                        'NIST SP 800-53 AC-17',
                                        'NIST SP 800-53 AC-19',
                                        'NIST SP 800-53 AC-20',
                                        'NIST SP 800-53 SC-15',
                                        'AICPA TSC CC6.6',
                                        'ISO 27001:2013 A.6.2.1',
                                        'ISO 27001:2013 A.6.2.2',
                                        'ISO 27001:2013 A.11.2.6',
                                        'ISO 27001:2013 A.13.1.1',
                                        'ISO 27001:2013 A.13.2.1'
                                    ]
                                },
                                'Workflow': {
                                    'Status': 'RESOLVED'
                                },
                                'RecordState': 'ARCHIVED'
                            }
                        ]
                    )
                    print(response)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

def eks_latest_k8s_version_check():
    # loop through EKS clusters
    response = eks.list_clusters(maxResults=100)
    myEksClusters = response['clusters']
    for clusters in myEksClusters:
        cluster = str(clusters)
        try:
            response = eks.describe_cluster(name=cluster)
            clusterName = str(response['cluster']['name'])
            clusterArn = str(response['cluster']['arn'])
            k8sVersionCheck = str(response['cluster']['version'])
            if k8sVersionCheck != '1.14' or '1.15':
                try:
                    # ISO Time
                    iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                    # create Sec Hub finding
                    response = securityhub.batch_import_findings(
                        Findings=[
                            {
                                'SchemaVersion': '2018-10-08',
                                'Id': clusterArn + '/eks-latest-k8s-version-check',
                                'ProductArn': 'arn:aws-us-gov:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                                'GeneratorId': clusterName,
                                'AwsAccountId': awsAccountId,
                                'Types': [ 'Software and Configuration Checks/AWS Security Best Practices', ],
                                'FirstObservedAt': iso8601Time,
                                'CreatedAt': iso8601Time,
                                'UpdatedAt': iso8601Time,
                                'Severity': { 'Label': 'MEDIUM' },
                                'Confidence': 99,
                                'Title': '[EKS.2] Elastic Kubernetes Service (EKS) clusters should use the latest Kubernetes version',
                                'Description': 'Elastic Kubernetes Service (EKS) cluster ' + clusterName + ' is using Kubernetes version ' + k8sVersionCheck + '. Refer to the remediation instructions if this configuration is not intended',
                                'Remediation': {
                                    'Recommendation': {
                                        'Text': 'Unless your application requires a specific version of Kubernetes, AWS recommends you choose the latest available Kubernetes version supported by Amazon EKS for your clusters. For upgrade information refer to the Updating an Amazon EKS Cluster Kubernetes Version section of the EKS user guide',
                                        'Url': 'https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html'
                                    }
                                },
                                'ProductFields': {
                                    'Product Name': 'ElectricEye'
                                },
                                'Resources': [
                                    {
                                        'Type': 'AwsEksCluster',
                                        'Id': clusterArn,
                                        'Partition': 'aws-us-gov',
                                        'Region': awsRegion,
                                        'Details': {
                                            'Other': { 'Cluster Name': clusterName }
                                        }
                                    }
                                ],
                                'Compliance': { 
                                    'Status': 'FAILED',
                                    'RelatedRequirements': [
                                        'NIST CSF ID.AM-2',
                                        'NIST SP 800-53 CM-8',
                                        'NIST SP 800-53 PM-5',
                                        'AICPA TSC CC3.2',
                                        'AICPA TSC CC6.1',
                                        'ISO 27001:2013 A.8.1.1',
                                        'ISO 27001:2013 A.8.1.2',
                                        'ISO 27001:2013 A.12.5.1'
                                    ]
                                },
                                'Workflow': {
                                    'Status': 'NEW'
                                },
                                'RecordState': 'ACTIVE'
                            }
                        ]
                    )
                    print(response)
                except Exception as e:
                    print(e)
            else:
                try:
                    # ISO Time
                    iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                    # create Sec Hub finding
                    response = securityhub.batch_import_findings(
                        Findings=[
                            {
                                'SchemaVersion': '2018-10-08',
                                'Id': clusterArn + '/eks-latest-k8s-version-check',
                                'ProductArn': 'arn:aws-us-gov:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                                'GeneratorId': clusterName,
                                'AwsAccountId': awsAccountId,
                                'Types': [ 'Software and Configuration Checks/AWS Security Best Practices', ],
                                'FirstObservedAt': iso8601Time,
                                'CreatedAt': iso8601Time,
                                'UpdatedAt': iso8601Time,
                                'Severity': { 'Label': 'INFORMATIONAL' },
                                'Confidence': 99,
                                'Title': '[EKS.2] Elastic Kubernetes Service (EKS) clusters should use the latest Kubernetes version',
                                'Description': 'Elastic Kubernetes Service (EKS) cluster ' + clusterName + ' is using Kubernetes version ' + k8sVersionCheck,
                                'Remediation': {
                                    'Recommendation': {
                                        'Text': 'Unless your application requires a specific version of Kubernetes, AWS recommends you choose the latest available Kubernetes version supported by Amazon EKS for your clusters. For upgrade information refer to the Updating an Amazon EKS Cluster Kubernetes Version section of the EKS user guide',
                                        'Url': 'https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html'
                                    }
                                },
                                'ProductFields': {
                                    'Product Name': 'ElectricEye'
                                },
                                'Resources': [
                                    {
                                        'Type': 'AwsEksCluster',
                                        'Id': clusterArn,
                                        'Partition': 'aws-us-gov',
                                        'Region': awsRegion,
                                        'Details': {
                                            'Other': { 'Cluster Name': clusterName }
                                        }
                                    }
                                ],
                                'Compliance': { 
                                    'Status': 'PASSED',
                                    'RelatedRequirements': [
                                        'NIST CSF ID.AM-2',
                                        'NIST SP 800-53 CM-8',
                                        'NIST SP 800-53 PM-5',
                                        'AICPA TSC CC3.2',
                                        'AICPA TSC CC6.1',
                                        'ISO 27001:2013 A.8.1.1',
                                        'ISO 27001:2013 A.8.1.2',
                                        'ISO 27001:2013 A.12.5.1'
                                    ]
                                },
                                'Workflow': {
                                    'Status': 'RESOLVED'
                                },
                                'RecordState': 'ARCHIVED'
                            }
                        ]
                    )
                    print(response)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

def eks_logging_audit_auth_check():
    # loop through EKS clusters
    response = eks.list_clusters(maxResults=100)
    myEksClusters = response['clusters']
    for clusters in myEksClusters:
        cluster = str(clusters)
        try:
            response = eks.describe_cluster(name=cluster)
            clusterName = str(response['cluster']['name'])
            clusterArn = str(response['cluster']['arn'])
            logInfo =  response['cluster']['logging']['clusterLogging']
            for logs in logInfo:
                logTypes = logs['types']
                enableCheck = str(logs['enabled'])
                if enableCheck == 'True':
                    for logs in logTypes:
                        if str(logs) == 'authenticator' and 'audit':
                            try:
                                # ISO Time
                                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                                # create Sec Hub finding
                                response = securityhub.batch_import_findings(
                                    Findings=[
                                        {
                                            'SchemaVersion': '2018-10-08',
                                            'Id': clusterArn + '/eks-logging-audit-auth-check',
                                            'ProductArn': 'arn:aws-us-gov:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                                            'GeneratorId': clusterName,
                                            'AwsAccountId': awsAccountId,
                                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices', ],
                                            'FirstObservedAt': iso8601Time,
                                            'CreatedAt': iso8601Time,
                                            'UpdatedAt': iso8601Time,
                                            'Severity': { 'Label': 'INFORMATIONAL' },
                                            'Confidence': 99,
                                            'Title': '[EKS.3] Elastic Kubernetes Service (EKS) clusters should have authenticator and/or audit logging enabled',
                                            'Description': 'Elastic Kubernetes Service (EKS) cluster ' + clusterName + ' has authenticator and audit logging enabled.',
                                            'Remediation': {
                                                'Recommendation': {
                                                    'Text': 'To enable logging for your cluster refer to the Amazon EKS Control Plane Logging section of the EKS user guide',
                                                    'Url': 'https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html'
                                                }
                                            },
                                            'ProductFields': {
                                                'Product Name': 'ElectricEye'
                                            },
                                            'Resources': [
                                                {
                                                    'Type': 'AwsEksCluster',
                                                    'Id': clusterArn,
                                                    'Partition': 'aws-us-gov',
                                                    'Region': awsRegion,
                                                    'Details': {
                                                        'Other': { 'Cluster Name': clusterName }
                                                    }
                                                }
                                            ],
                                            'Compliance': { 
                                                'Status': 'PASSED',
                                                'RelatedRequirements': [
                                                    'NIST CSF DE.AE-3',
                                                    'NIST SP 800-53 AU-6',
                                                    'NIST SP 800-53 CA-7',
                                                    'NIST SP 800-53 IR-4',
                                                    'NIST SP 800-53 IR-5',
                                                    'NIST SP 800-53 IR-8', 
                                                    'NIST SP 800-53 SI-4',
                                                    'AICPA TSC CC7.2',
                                                    'ISO 27001:2013 A.12.4.1',
                                                    'ISO 27001:2013 A.16.1.7'
                                                ]
                                            },
                                            'Workflow': {
                                                'Status': 'RESOLVED'
                                            },
                                            'RecordState': 'ACTIVE'
                                        }
                                    ]
                                )
                                print(response)
                            except Exception as e:
                                print(e)
                        else:
                            try:
                                # ISO Time
                                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                                # create Sec Hub finding
                                response = securityhub.batch_import_findings(
                                    Findings=[
                                        {
                                            'SchemaVersion': '2018-10-08',
                                            'Id': clusterArn + '/eks-logging-audit-auth-check',
                                            'ProductArn': 'arn:aws-us-gov:securityhub:' + awsRegion + ':' + awsAccountId + ':product/' + awsAccountId + '/default',
                                            'GeneratorId': clusterName,
                                            'AwsAccountId': awsAccountId,
                                            'Types': [ 'Software and Configuration Checks/AWS Security Best Practices', ],
                                            'FirstObservedAt': iso8601Time,
                                            'CreatedAt': iso8601Time,
                                            'UpdatedAt': iso8601Time,
                                            'Severity': { 'Label': 'MEDIUM' },
                                            'Confidence': 99,
                                            'Title': '[EKS.3] Elastic Kubernetes Service (EKS) clusters should have authenticator and/or audit logging enabled',
                                            'Description': 'Elastic Kubernetes Service (EKS) cluster ' + clusterName + ' does not have authenticator or audit logging enabled. Refer to the remediation instructions if this configuration is not intended',
                                            'Remediation': {
                                                'Recommendation': {
                                                    'Text': 'To enable logging for your cluster refer to the Amazon EKS Control Plane Logging section of the EKS user guide',
                                                    'Url': 'https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html'
                                                }
                                            },
                                            'ProductFields': {
                                                'Product Name': 'ElectricEye'
                                            },
                                            'Resources': [
                                                {
                                                    'Type': 'AwsEksCluster',
                                                    'Id': clusterArn,
                                                    'Partition': 'aws-us-gov',
                                                    'Region': awsRegion,
                                                    'Details': {
                                                        'Other': { 'Cluster Name': clusterName }
                                                    }
                                                }
                                            ],
                                            'Compliance': { 
                                                'Status': 'FAILED',
                                                'RelatedRequirements': [
                                                    'NIST CSF DE.AE-3',
                                                    'NIST SP 800-53 AU-6',
                                                    'NIST SP 800-53 CA-7',
                                                    'NIST SP 800-53 IR-4',
                                                    'NIST SP 800-53 IR-5',
                                                    'NIST SP 800-53 IR-8', 
                                                    'NIST SP 800-53 SI-4',
                                                    'AICPA TSC CC7.2',
                                                    'ISO 27001:2013 A.12.4.1',
                                                    'ISO 27001:2013 A.16.1.7'
                                                ]
                                            },
                                            'Workflow': {
                                                'Status': 'NEW'
                                            },
                                            'RecordState': 'ACTIVE'
                                        }
                                    ]
                                )
                                print(response)
                            except Exception as e:
                                print(e)
        except Exception as e:
            print(e)

def eks_auditor():
    eks_public_endpoint_access_check()
    eks_latest_k8s_version_check()
    eks_logging_audit_auth_check()

eks_auditor()