run: initdb sync
	@python3 app/app.py

initdb:
	@db/init_db.sh

sync: 
	@python3 app/data_init.py

clean:
	@rm -rf db/*.db db/log/violations.csv db/log/new_violations.csv db/log/deleted_violations.csv db/log/updated_violations.csv