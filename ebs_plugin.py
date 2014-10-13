import boto
import boto.ec2
import sys

from boundary_aws_plugin.cloudwatch_plugin import CloudwatchPlugin
from boundary_aws_plugin.cloudwatch_metrics import CloudwatchMetrics


class EbsCloudwatchMetrics(CloudwatchMetrics):
    def __init__(self, access_key_id, secret_access_key):
        return super(EbsCloudwatchMetrics, self).__init__(access_key_id, secret_access_key, 'AWS/EBS')

    def get_region_list(self):
        # Some regions are returned that actually do not support EC2.  Skip those.
        return [r for r in boto.ec2.regions() if r.name not in ['cn-north-1', 'us-gov-west-1']]

    def get_entities_for_region(self, region):
        ec2 = boto.connect_ec2(self.access_key_id, self.secret_access_key, region=region)
        return ec2.get_all_volumes()

    def get_entity_dimensions(self, region, volume):
        return dict(VolumeId=volume.id)

    def get_entity_source_name(self, volume):
        return volume.id

    def get_metric_list(self):
        return (
            ('VolumeReadBytes', 'Sum', 'AWS_EBS_VOLUME_READ_BYTES'),
            ('VolumeWriteBytes', 'Sum', 'AWS_EBS_VOLUME_WRITE_BYTES'),
            ('VolumeReadOps', 'Sum', 'AWS_EBS_VOLUME_READ_OPS'),
            ('VolumeWriteOps', 'Sum', 'AWS_EBS_VOLUME_WRITE_OPS'),
            ('VolumeTotalReadTime', 'Sum', 'AWS_EBS_VOLUME_TOTAL_READ_TIME'),
            ('VolumeTotalWriteTime', 'Sum', 'AWS_EBS_VOLUME_TOTAL_WRITE_TIME'),
            ('VolumeIdleTime', 'Sum', 'AWS_EBS_VOLUME_IDLE_TIME'),
            ('VolumeQueueLength', 'Sum', 'AWS_EBS_VOLUME_QUEUE_LENGTH'),
            ('VolumeThroughputPercentage', 'Sum', 'AWS_EBS_VOLUME_THROUGHPUT_PERCENTAGE'),
            ('VolumeConsumedReadWriteOps', 'Sum', 'AWS_EBS_VOLUME_CONSUMED_READ_WRITE_OPS'),
        )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        import logging
        logging.basicConfig(level=logging.INFO)

    plugin = CloudwatchPlugin(EbsCloudwatchMetrics, '', 'boundary-plugin-aws-ebs-python-status')
    plugin.main()

