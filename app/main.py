from fastapi import FastAPI, HTTPException, Body, File, UploadFile, Form
from pydantic import BaseModel
from .portainer_service import portainer_service

# Pydantic models for request bodies
class UserCreate(BaseModel):
    username: str
    password: str
    role: int = 2

class TeamCreate(BaseModel):
    name: str

class TeamMembershipCreate(BaseModel):
    user_id: int
    role: int = 2

class KubernetesAppCreate(BaseModel):
    name: str
    manifest: str # The YAML content

class KubernetesAppUpdate(BaseModel):
    manifest: str # The YAML content

class StackFromRepositoryCreate(BaseModel):
    name: str
    repository_url: str
    repository_reference_name: str = "refs/heads/main"
    compose_file: str = "docker-compose.yml"
    endpoint_id: int = 1
    repository_authentication: bool = False
    repository_username: str | None = None
    repository_password: str | None = None


app = FastAPI(
    title="MCP Portainer API",
    description="API para gerenciar o Portainer CE.",
    version="0.1.0",
)

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.get("/api/v1/stacks", tags=["Stacks"])
def get_stacks(endpoint_id: int = 3):
    try:
        return portainer_service.get_stacks(endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stacks/{stack_id}", tags=["Stacks"])
def get_stack(stack_id: int):
    try:
        return portainer_service.get_stack(stack_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stacks/{stack_id}/file", tags=["Stacks"])
def get_stack_file(stack_id: int):
    try:
        return portainer_service.get_stack_file(stack_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/stacks/string", tags=["Stacks"])
def create_stack_from_string(name: str, stack_file_content: str = Body(..., embed=True), endpoint_id: int = 1):
    try:
        return portainer_service.create_stack_from_string(name, stack_file_content, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/stacks/file", tags=["Stacks"])
async def create_stack_from_file(
    name: str = Form(...),
    endpoint_id: int = Form(1),
    file: UploadFile = File(...)
):
    try:
        file_content = await file.read()
        return portainer_service.create_stack_from_file(name, file_content, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/stacks/repository", tags=["Stacks"])
def create_stack_from_repository(stack: StackFromRepositoryCreate):
    try:
        return portainer_service.create_stack_from_repository(
            name=stack.name,
            repository_url=stack.repository_url,
            repository_reference_name=stack.repository_reference_name,
            compose_file=stack.compose_file,
            endpoint_id=stack.endpoint_id,
            repository_authentication=stack.repository_authentication,
            repository_username=stack.repository_username,
            repository_password=stack.repository_password,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/stacks/{stack_id}", tags=["Stacks"])
def update_stack(stack_id: int, stack_file_content: str = Body(..., embed=True), endpoint_id: int = 1):
    try:
        return portainer_service.update_stack(stack_id, stack_file_content, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/stacks/{stack_id}", tags=["Stacks"])
def delete_stack(stack_id: int, endpoint_id: int = 1):
    try:
        return portainer_service.delete_stack(stack_id, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/endpoints", tags=["Portainer"])
def get_endpoints():
    try:
        return portainer_service.get_endpoints()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/containers", tags=["Containers"])
def get_containers(endpoint_id: int = 1):
    try:
        return portainer_service.get_containers(endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/containers/{container_id}/start", tags=["Containers"])
def start_container(container_id: str, endpoint_id: int = 1):
    try:
        return portainer_service.start_container(container_id, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/containers/{container_id}/stop", tags=["Containers"])
def stop_container(container_id: str, endpoint_id: int = 1):
    try:
        return portainer_service.stop_container(container_id, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/containers/{container_id}/restart", tags=["Containers"])
def restart_container(container_id: str, endpoint_id: int = 1):
    try:
        return portainer_service.restart_container(container_id, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Images
@app.get("/api/v1/images", tags=["Images"])
def get_images(endpoint_id: int = 1):
    try:
        return portainer_service.get_images(endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/images/pull", tags=["Images"])
def pull_image(from_image: str, tag: str = "latest", endpoint_id: int = 1):
    try:
        return portainer_service.pull_image(from_image, tag, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/images/{image_id:path}", tags=["Images"])
def remove_image(image_id: str, endpoint_id: int = 1):
    try:
        return portainer_service.remove_image(image_id, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Volumes
@app.get("/api/v1/volumes", tags=["Volumes"])
def get_volumes(endpoint_id: int = 1):
    try:
        return portainer_service.get_volumes(endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/volumes", tags=["Volumes"])
def create_volume(name: str, driver: str = "local", endpoint_id: int = 1):
    try:
        return portainer_service.create_volume(name, driver, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/volumes/{volume_id}", tags=["Volumes"])
def remove_volume(volume_id: str, endpoint_id: int = 1):
    try:
        return portainer_service.remove_volume(volume_id, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Networks
@app.get("/api/v1/networks", tags=["Networks"])
def get_networks(endpoint_id: int = 1):
    try:
        return portainer_service.get_networks(endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/networks", tags=["Networks"])
def create_network(name: str, driver: str = "bridge", endpoint_id: int = 1):
    try:
        return portainer_service.create_network(name, driver, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/networks/{network_id}", tags=["Networks"])
def remove_network(network_id: str, endpoint_id: int = 1):
    try:
        return portainer_service.remove_network(network_id, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Users & Teams
@app.get("/api/v1/users", tags=["Users & Teams"])
def get_users():
    try:
        return portainer_service.get_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/users", tags=["Users & Teams"])
def create_user(user: UserCreate):
    try:
        return portainer_service.create_user(user.username, user.password, user.role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/users/{user_id}", tags=["Users & Teams"])
def delete_user(user_id: int):
    try:
        return portainer_service.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/teams", tags=["Users & Teams"])
def get_teams():
    try:
        return portainer_service.get_teams()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/teams", tags=["Users & Teams"])
def create_team(team: TeamCreate):
    try:
        return portainer_service.create_team(team.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/teams/{team_id}", tags=["Users & Teams"])
def delete_team(team_id: int):
    try:
        return portainer_service.delete_team(team_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/teams/{team_id}/members", tags=["Users & Teams"])
def add_user_to_team(team_id: int, membership: TeamMembershipCreate):
    try:
        return portainer_service.add_user_to_team(team_id, membership.user_id, membership.role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/teams/{team_id}/members/{user_id}", tags=["Users & Teams"])
def remove_user_from_team(team_id: int, user_id: int):
    try:
        return portainer_service.remove_user_from_team(team_id, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Kubernetes
@app.get("/api/v1/kubernetes/{endpoint_id}/nodes", tags=["Kubernetes"])
def get_kubernetes_nodes(endpoint_id: int):
    try:
        return portainer_service.get_kubernetes_nodes(endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/kubernetes/{endpoint_id}/namespaces", tags=["Kubernetes"])
def get_kubernetes_namespaces(endpoint_id: int):
    try:
        return portainer_service.get_kubernetes_namespaces(endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/kubernetes/{endpoint_id}/pods", tags=["Kubernetes"])
def get_kubernetes_pods(endpoint_id: int, namespace: str = None):
    try:
        return portainer_service.get_kubernetes_pods(endpoint_id, namespace)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/kubernetes/{endpoint_id}/deployments", tags=["Kubernetes"])
def get_kubernetes_deployments(endpoint_id: int, namespace: str = None):
    try:
        return portainer_service.get_kubernetes_deployments(endpoint_id, namespace)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/kubernetes/{endpoint_id}/services", tags=["Kubernetes"])
def get_kubernetes_services(endpoint_id: int, namespace: str = None):
    try:
        return portainer_service.get_kubernetes_services(endpoint_id, namespace)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/kubernetes/{endpoint_id}/apps", tags=["Kubernetes"])
def get_kubernetes_applications(endpoint_id: int):
    try:
        return portainer_service.get_kubernetes_applications(endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/kubernetes/{endpoint_id}/apps", tags=["Kubernetes"])
def create_kubernetes_application(endpoint_id: int, app_data: KubernetesAppCreate):
    try:
        return portainer_service.create_kubernetes_application(app_data.name, app_data.manifest, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/kubernetes/{endpoint_id}/apps/{app_id}", tags=["Kubernetes"])
def update_kubernetes_application(endpoint_id: int, app_id: int, app_data: KubernetesAppUpdate):
    try:
        # The service method for update is the generic update_stack
        return portainer_service.update_stack(app_id, app_data.manifest, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/kubernetes/{endpoint_id}/apps/{app_id}", tags=["Kubernetes"])
def delete_kubernetes_application(endpoint_id: int, app_id: int):
    try:
        # The service method for delete is the generic delete_stack
        return portainer_service.delete_stack(app_id, endpoint_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
