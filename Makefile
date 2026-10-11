.PHONY: up down logs ps test

up:
	@test -f .env || cp .env.example .env
	docker compose up -d --build --wait

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

test:
	@echo "== /healthz =="
	@curl -s http://localhost:8080/healthz | jq .
	@echo "== X-Request-ID generated when missing =="
	@curl -si http://localhost:8080/healthz | grep -i '^x-request-id'
	@echo "== X-Request-ID passed through =="
	@curl -si -H 'X-Request-ID: my-id-123' http://localhost:8080/healthz | grep -i '^x-request-id'
	@echo "== Flood test: 20 parallel requests (expect some 429) =="
	@sleep 1
	@seq 1 20 | xargs -P 20 -I{} curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/healthz | sort | uniq -c