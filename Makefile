PYTHON ?= python3

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

train:
	python train.py

eval:
	echo "## Model Metrics" > report.md
	cat ./Results/metrics.txt >> report.md
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
	cml comment create report.md

update-main:
	git config --global user.name $(USER_NAME)
	git config --global user.email $(USER_EMAIL)
	git add Results/ Model/
	git commit -m "Update results and model"
	git push origin main


update-branch:
	git config --global user.name $(USER_NAME)
	git config --global user.email $(USER_EMAIL)
	git commit -am "Update with new results"
	git push --force origin HEAD:update

hf-login:
	git pull origin update
	git switch update
	$(PYTHON) -m pip install -U "huggingface_hub[cli]"
	test -n "$(HF)" || (echo "HF token is required" && exit 1)
	hf auth login --token "$(HF)" --add-to-git-credential

push-hub:
	hf upload asishjose/Drug-Classification README.md README.md --repo-type=space --commit-message="Sync Space metadata"
	hf upload asishjose/Drug-Classification ./App App --repo-type=space --commit-message="Sync App files"
	hf upload asishjose/Drug-Classification ./Model Model --repo-type=space --commit-message="Sync Model"
	hf upload asishjose/Drug-Classification ./Results Results --repo-type=space --commit-message="Sync Metrics"

deploy: hf-login push-hub
