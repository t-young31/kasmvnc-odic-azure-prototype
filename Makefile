SHELL:=/bin/bash
.PHONY: ssl

deploy: ssl
	. load_env.sh && \
	docker compose up --build

destroy:
	docker compose down

ssl:
	. load_env.sh && \
	./ssl/create_if_required.sh
