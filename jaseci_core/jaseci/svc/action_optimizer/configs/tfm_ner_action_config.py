TFM_NER_ACTION_CONFIG = {
    "module": "jaseci_ai_kit.tfm_ner",
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "tfm-ner", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "tfm-ner"},
                "type": "ClusterIP",
                "sessionAffinity": "None",
                "internalTrafficPolicy": "Cluster",
            },
            "status": {"loadBalancer": {}},
        },
        "ConfigMap": {
            "kind": "ConfigMap",
            "apiVersion": "v1",
            "metadata": {
                "name": "tfm-ner-up",
                "namespace": "default",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "git clone https://github.com/Jaseci-Labs/jaseci.git /jaseci/\npip install datasets\ncd /jaseci/jaseci_core/\nsource install.sh\ncd /jaseci/jaseci_ai_kit/\nsource install.sh\ncd /jaseci/jaseci_ai_kit/jaseci_ai_kit/modules/tfm_ner\nuvicorn jaseci_ai_kit.tfm_ner:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "tfm-ner", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "tfm-ner"}},
                "template": {
                    "metadata": {
                        "name": "tfm-ner",
                        "creationTimestamp": None,
                        "labels": {"pod": "tfm-ner"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {"name": "tfm-ner-up", "defaultMode": 420},
                            }
                        ],
                        "containers": [
                            {
                                "name": "tfm-ner",
                                "image": "jaseci/jaseci-ai-kit:latest",
                                "command": ["bash", "-c", "source script/prod_up"],
                                "ports": [{"containerPort": 80, "protocol": "TCP"}],
                                "resources": {
                                    "limits": {"memory": "3Gi"},
                                    "requests": {"memory": "3Gi"},
                                },
                                "volumeMounts": [
                                    {"name": "prod-script", "mountPath": "/script"}
                                ],
                                "terminationMessagePath": "/dev/termination-log",
                                "terminationMessagePolicy": "File",
                                "imagePullPolicy": "IfNotPresent",
                            }
                        ],
                        "restartPolicy": "Always",
                        "terminationGracePeriodSeconds": 30,
                        "dnsPolicy": "ClusterFirst",
                        "securityContext": {},
                        "schedulerName": "default-scheduler",
                    },
                },
                "strategy": {
                    "type": "RollingUpdate",
                    "rollingUpdate": {"maxUnavailable": "25%", "maxSurge": "25%"},
                },
                "revisionHistoryLimit": 10,
                "progressDeadlineSeconds": 600,
            },
            "status": {},
        },
    },
}