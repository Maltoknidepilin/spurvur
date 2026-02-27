.PHONY: completion-install completion-install-dry-run completion-uninstall completion-uninstall-dry-run completion-setup-datadir custom-plugins-install

completion-install:
	./scripts/install-shell-completion.sh

completion-install-dry-run:
	./scripts/install-shell-completion.sh --dry-run

completion-uninstall:
	./scripts/uninstall-shell-completion.sh

completion-uninstall-dry-run:
	./scripts/uninstall-shell-completion.sh --dry-run

completion-setup-datadir:
	uv run --project . sparv setup --dir "$(CURDIR)/.sparv-data"

custom-plugins-install:
	./scripts/install-local-custom-plugins.sh
