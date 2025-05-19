# Basic Docker commands
build_image:
	docker build -t swift-bill .

run_container:
	docker run -d --name swift-bill-container -v .:/app -p 8000:8000 swift-bill

# Add helpful commands for Docker management
stop_container:
	docker stop swift-bill-container

remove_container:
	docker rm swift-bill-container

# Clean up command
clean: stop_container remove_container
	docker rmi swift-bill

# Development commands
dev: build_image run_container

# Restart command
restart: stop_container remove_container run_container

# Show container logs
logs:
	docker logs -f swift-bill-container

# Show container status
status:
	docker ps -a | grep swift-bill

.PHONY: build_image run_container stop_container remove_container clean dev restart logs status