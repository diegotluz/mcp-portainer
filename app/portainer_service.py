import requests
from .config import settings

class PortainerService:
    def __init__(self):
        self.portainer_url = settings.portainer_url
        self.headers = {
            "X-API-Key": settings.portainer_api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_stacks(self, endpoint_id=1):
        response = requests.get(f"{self.portainer_url}/api/stacks?endpointId={endpoint_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_endpoints(self):
        response = requests.get(f"{self.portainer_url}/api/endpoints", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_containers(self, endpoint_id=1):
        response = requests.get(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/containers/json", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def start_container(self, container_id, endpoint_id=1):
        response = requests.post(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}/start", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def stop_container(self, container_id, endpoint_id=1):
        response = requests.post(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}/stop", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def restart_container(self, container_id, endpoint_id=1):
        response = requests.post(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}/restart", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_stack(self, stack_id):
        response = requests.get(f"{self.portainer_url}/api/stacks/{stack_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_stack_file(self, stack_id):
        response = requests.get(f"{self.portainer_url}/api/stacks/{stack_id}/file", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_stack_from_string(self, name, stack_file_content, endpoint_id=1):
        params = {
            "endpointId": endpoint_id
        }
        data = {
            "Name": name,
            "StackFileContent": stack_file_content,
        }
        response = requests.post(f"{self.portainer_url}/api/stacks/create/standalone/string", headers=self.headers, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def create_stack_from_file(self, name, file_content, endpoint_id=1):
        params = {
            "endpointId": endpoint_id
        }
        stack_file_content = file_content.decode('utf-8')
        data = {
            "Name": name,
            "StackFileContent": stack_file_content,
        }

        response = requests.post(f"{self.portainer_url}/api/stacks/create/standalone/string", headers=self.headers, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def create_stack_from_repository(self, name, repository_url, repository_reference_name, compose_file, endpoint_id=1, repository_authentication=False, repository_username=None, repository_password=None):
        params = {
            "type": 2,  # Standalone Docker Compose
            "method": "repository",
            "endpointId": endpoint_id
        }
        data = {
            "name": name,
            "repositoryUrl": repository_url,
            "repositoryReferenceName": repository_reference_name,
            "composeFile": compose_file,
            "repositoryAuthentication": repository_authentication,
            "repositoryUsername": repository_username,
            "repositoryPassword": repository_password
        }
        # Remove null values from data
        data = {k: v for k, v in data.items() if v is not None}

        response = requests.post(f"{self.portainer_url}/api/stacks", headers=self.headers, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def update_stack(self, stack_id, stack_file_content, endpoint_id=1):
        params = {
            "endpointId": endpoint_id
        }
        data = {
            "stackFileContent": stack_file_content
        }
        response = requests.put(f"{self.portainer_url}/api/stacks/{stack_id}", headers=self.headers, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def delete_stack(self, stack_id, endpoint_id=1):
        params = {
            "endpointId": endpoint_id
        }
        response = requests.delete(f"{self.portainer_url}/api/stacks/{stack_id}", headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    # Images
    def get_images(self, endpoint_id=1):
        response = requests.get(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/images/json", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def pull_image(self, from_image, tag, endpoint_id=1):
        params = {
            "fromImage": from_image,
            "tag": tag
        }
        response = requests.post(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/images/create", headers=self.headers, params=params)
        response.raise_for_status()
        # This endpoint returns a stream, we'll just return the success status
        return {"status": "pull request sent"}

    def remove_image(self, image_id, endpoint_id=1):
        response = requests.delete(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/images/{image_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    # Volumes
    def get_volumes(self, endpoint_id=1):
        response = requests.get(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/volumes", headers=self.headers)
        response.raise_for_status()
        return response.json().get("Volumes", [])

    def create_volume(self, name, driver="local", endpoint_id=1):
        data = {
            "Name": name,
            "Driver": driver
        }
        response = requests.post(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/volumes/create", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def remove_volume(self, volume_id, endpoint_id=1):
        response = requests.delete(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/volumes/{volume_id}", headers=self.headers)
        # Returns 204 on success, no json body
        response.raise_for_status()
        return {"status": "deleted"}

    # Networks
    def get_networks(self, endpoint_id=1):
        response = requests.get(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/networks", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_network(self, name, driver="bridge", endpoint_id=1):
        data = {
            "Name": name,
            "Driver": driver
        }
        response = requests.post(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/networks/create", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def remove_network(self, network_id, endpoint_id=1):
        response = requests.delete(f"{self.portainer_url}/api/endpoints/{endpoint_id}/docker/networks/{network_id}", headers=self.headers)
        # Returns 204 on success, no json body
        response.raise_for_status()
        return {"status": "deleted"}

    # Users
    def get_users(self):
        response = requests.get(f"{self.portainer_url}/api/users", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_user(self, username, password, role=2):
        data = {
            "username": username,
            "password": password,
            "role": role
        }
        response = requests.post(f"{self.portainer_url}/api/users", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id):
        response = requests.delete(f"{self.portainer_url}/api/users/{user_id}", headers=self.headers)
        # Returns 204 on success
        response.raise_for_status()
        return {"status": "deleted"}

    # Teams
    def get_teams(self):
        response = requests.get(f"{self.portainer_url}/api/teams", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_team(self, name):
        data = {
            "name": name
        }
        response = requests.post(f"{self.portainer_url}/api/teams", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_team(self, team_id):
        response = requests.delete(f"{self.portainer_url}/api/teams/{team_id}", headers=self.headers)
        # Returns 204 on success
        response.raise_for_status()
        return {"status": "deleted"}

    def get_team_memberships(self, team_id):
        response = requests.get(f"{self.portainer_url}/api/teams/{team_id}/memberships", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def add_user_to_team(self, team_id, user_id, role=2):
        data = {
            "userID": user_id,
            "role": role
        }
        response = requests.post(f"{self.portainer_url}/api/teams/{team_id}/memberships", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def remove_user_from_team(self, team_id, user_id):
        # First, find the membership ID for the user in the team
        memberships = self.get_team_memberships(team_id)
        membership_id = None
        for member in memberships:
            if member["UserID"] == user_id:
                membership_id = member["Id"]
                break
        
        if not membership_id:
            raise Exception("User is not a member of the team")

        response = requests.delete(f"{self.portainer_url}/api/teams/{team_id}/memberships/{membership_id}", headers=self.headers)
        # Returns 204 on success
        response.raise_for_status()
        return {"status": "deleted"}

    # Kubernetes
    def _get_k8s_resource(self, endpoint_id, resource_path):
        """Helper function to query the Kubernetes API through Portainer."""
        url = f"{self.portainer_url}/api/endpoints/{endpoint_id}/kubernetes/{resource_path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_kubernetes_nodes(self, endpoint_id):
        return self._get_k8s_resource(endpoint_id, "api/v1/nodes")

    def get_kubernetes_namespaces(self, endpoint_id):
        return self._get_k8s_resource(endpoint_id, "api/v1/namespaces")

    def get_kubernetes_pods(self, endpoint_id, namespace=None):
        if namespace:
            path = f"api/v1/namespaces/{namespace}/pods"
        else:
            path = "api/v1/pods"
        return self._get_k8s_resource(endpoint_id, path)

    def get_kubernetes_deployments(self, endpoint_id, namespace=None):
        if namespace:
            path = f"apis/apps/v1/namespaces/{namespace}/deployments"
        else:
            path = "apis/apps/v1/deployments"
        return self._get_k8s_resource(endpoint_id, path)

    def get_kubernetes_services(self, endpoint_id, namespace=None):
        if namespace:
            path = f"api/v1/namespaces/{namespace}/services"
        else:
            path = "api/v1/services"
        return self._get_k8s_resource(endpoint_id, path)

    def get_kubernetes_applications(self, endpoint_id):
        all_stacks = self.get_stacks(endpoint_id)
        kubernetes_apps = [stack for stack in all_stacks if stack.get("Type") == 2]
        return kubernetes_apps

    def create_kubernetes_application(self, name, manifest_content, endpoint_id):
        data = {
            "name": name,
            "stackFileContent": manifest_content,
        }
        # type=2 for Kubernetes
        response = requests.post(f"{self.portainer_url}/api/stacks?type=2&method=string&endpointId={endpoint_id}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

portainer_service = PortainerService()
