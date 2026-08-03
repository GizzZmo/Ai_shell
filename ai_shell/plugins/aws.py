"""AWS CLI assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


AWS_SYSTEM_PROMPT = (
    "You are an expert AWS cloud administrator. The user has the `aws` CLI "
    "(and optionally `aws-vault` / SSO). Help them manage EC2, S3, IAM, Lambda, "
    "EKS, RDS, CloudFormation, VPC, CloudWatch, and other services. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Prefer read-only operations (`describe`, `list`, `get`) first. "
    "Always warn before delete, terminate, or high-cost operations. "
    "Remind the user to confirm the correct profile/region and account."
)


@register_plugin_class
class AwsPlugin(ToolPlugin):
    id = "aws"
    name = "AWS Assistant"
    description = "AI help for AWS CLI, EC2, S3, IAM, EKS and more"
    system_prompt = AWS_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("aws") is not None
