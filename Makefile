SHELL:=/bin/bash
.PHONY: ssl

deploy: ssl
	. load_env.sh && \
	docker compose up --build && \
	echo "http://localhost:4180/me"

destroy:
	docker compose down

ssl:
	. load_env.sh && \
	./ssl/create_if_required.sh
