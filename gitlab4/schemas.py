from __future__ import annotations

from typing import Any, Optional, List

from pydantic import BaseModel


class ProjectVariable(BaseModel):
    variable_type: str = 'env_var'
    key: str
    value: str
    protected: bool = False
    masked: bool = False
    raw: bool = False
    environment_scope: str = "*"
    description: str | None = None


class Namespace(BaseModel):
    id: int
    name: str
    path: str
    kind: str
    full_path: str
    parent_id: Any
    avatar_url: Any
    web_url: str


class _Links(BaseModel):
    self: str
    issues: str
    merge_requests: str
    repo_branches: str
    labels: str
    events: str
    members: str
    cluster_agents: str


class ContainerExpirationPolicy(BaseModel):
    cadence: str
    enabled: bool
    keep_n: int
    older_than: str
    name_regex: str
    name_regex_keep: Any
    next_run_at: str


class GroupAccess(BaseModel):
    access_level: int
    notification_level: int


class Permissions(BaseModel):
    project_access: Any
    group_access: GroupAccess


class Project(BaseModel):
    id: int
    description: Optional[str] = None
    name: str
    name_with_namespace: Optional[str] = None
    path: str
    path_with_namespace: Optional[str] = None
    created_at: str
    default_branch: Optional[str] = None
    tag_list: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    ssh_url_to_repo: Optional[str] = None
    http_url_to_repo: Optional[str] = None
    web_url: Optional[str] = None
    readme_url: Optional[str] = None
    forks_count: Optional[int] = None
    avatar_url: Optional[Any] = None
    star_count: Optional[int] = None
    last_activity_at: Optional[str] = None
    namespace: Optional[Namespace] = None
    container_registry_image_prefix: Optional[str] = None
    _links: Optional[_Links] = None
    code_suggestions: Optional[bool] = None
    packages_enabled: Optional[bool] = None
    empty_repo: Optional[bool] = None
    archived: Optional[bool] = None
    visibility: Optional[str] = None
    resolve_outdated_diff_discussions: Optional[bool] = None
    container_expiration_policy: Optional[ContainerExpirationPolicy] = None
    issues_enabled: Optional[bool] = None
    merge_requests_enabled: Optional[bool] = None
    wiki_enabled: Optional[bool] = None
    jobs_enabled: Optional[bool] = None
    snippets_enabled: Optional[bool] = None
    container_registry_enabled: Optional[bool] = None
    service_desk_enabled: Optional[bool] = None
    service_desk_address: Optional[str] = None
    can_create_merge_request_in: Optional[bool] = None
    issues_access_level: Optional[str] = None
    repository_access_level: Optional[str] = None
    merge_requests_access_level: Optional[str] = None
    forking_access_level: Optional[str] = None
    wiki_access_level: Optional[str] = None
    builds_access_level: Optional[str] = None
    snippets_access_level: Optional[str] = None
    pages_access_level: Optional[str] = None
    analytics_access_level: Optional[str] = None
    container_registry_access_level: Optional[str] = None
    security_and_compliance_access_level: Optional[str] = None
    releases_access_level: Optional[str] = None
    environments_access_level: Optional[str] = None
    feature_flags_access_level: Optional[str] = None
    infrastructure_access_level: Optional[str] = None
    monitor_access_level: Optional[str] = None
    model_experiments_access_level: Optional[str] = None
    model_registry_access_level: Optional[str] = None
    emails_disabled: Optional[bool] = None
    emails_enabled: Optional[bool] = None
    shared_runners_enabled: Optional[bool] = None
    lfs_enabled: Optional[bool] = None
    creator_id: Optional[int] = None
    import_url: Optional[Any] = None
    import_type: Optional[Any] = None
    import_status: Optional[str] = None
    import_error: Optional[Any] = None
    open_issues_count: Optional[int] = None
    description_html: Optional[str] = None
    updated_at: Optional[str] = None
    ci_default_git_depth: Optional[int] = None
    ci_forward_deployment_enabled: Optional[bool] = None
    ci_forward_deployment_rollback_allowed: Optional[bool] = None
    ci_job_token_scope_enabled: Optional[bool] = None
    ci_separated_caches: Optional[bool] = None
    ci_allow_fork_pipelines_to_run_in_parent_project: Optional[bool] = None
    build_git_strategy: Optional[str] = None
    keep_latest_artifact: Optional[bool] = None
    restrict_user_defined_variables: Optional[bool] = None
    runners_token: Optional[str] = None
    runner_token_expiration_interval: Optional[Any] = None
    group_runners_enabled: Optional[bool] = None
    auto_cancel_pending_pipelines: Optional[str] = None
    build_timeout: Optional[int] = None
    auto_devops_enabled: Optional[bool] = None
    auto_devops_deploy_strategy: Optional[str] = None
    ci_config_path: Optional[str] = None
    public_jobs: Optional[bool] = None
    shared_with_groups: Optional[List] = None
    only_allow_merge_if_pipeline_succeeds: Optional[bool] = None
    allow_merge_on_skipped_pipeline: Optional[Any] = None
    request_access_enabled: Optional[bool] = None
    only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None
    remove_source_branch_after_merge: Optional[bool] = None
    printing_merge_request_link_enabled: Optional[bool] = None
    merge_method: Optional[str] = None
    squash_option: Optional[str] = None
    enforce_auth_checks_on_uploads: Optional[bool] = None
    suggestion_commit_message: Optional[Any] = None
    merge_commit_template: Optional[Any] = None
    squash_commit_template: Optional[Any] = None
    issue_branch_template: Optional[Any] = None
    autoclose_referenced_issues: Optional[bool] = None
    approvals_before_merge: Optional[int] = None
    mirror: Optional[bool] = None
    external_authorization_classification_label: Optional[str] = None
    marked_for_deletion_at: Optional[Any] = None
    marked_for_deletion_on: Optional[Any] = None
    requirements_enabled: Optional[bool] = None
    requirements_access_level: Optional[str] = None
    security_and_compliance_enabled: Optional[bool] = None
    compliance_frameworks: Optional[List] = None
    issues_template: Optional[Any] = None
    merge_requests_template: Optional[Any] = None
    ci_restrict_pipeline_cancellation_role: Optional[str] = None
    merge_pipelines_enabled: Optional[bool] = None
    merge_trains_enabled: Optional[bool] = None
    merge_trains_skip_train_allowed: Optional[bool] = None
    allow_pipeline_trigger_approve_deployment: Optional[bool] = None
    permissions: Optional[Permissions] = None

