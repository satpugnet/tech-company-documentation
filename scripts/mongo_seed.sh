#!/usr/bin/env bash

# Insert basic seed documents inside mongo
mongo --eval 'db.document.insert({ "_id" : ObjectId("5d153eb82174f790d2fe6d1f"), "name" : "Mongo DB", "content" : "# Mongo\n\n## Connecting to DB\n\nRun the command\n\n```\nmake db\n```\n\nThis should start the mongo process (if not already started). Then, to connect to the DB, run\n\n```\nmongo\n```\n\nYou will enter the **mongo shell**, select the right database (our is called `documetation`)\n\n```\n> use documentation\n```\n\nOnce in the right database, you can view the different collections (equivalent of tables in mongo) by doing\n\n```\n> show collections\n```\n\nThere should be only 1 collection, called `document` if you have already created an object\n\nTo get all the documents from a the collection `document`, run\n\n```\n> db.document.find({})\n```\n\n## Explaination\n\nThe mongo client can be found in the `mongo/mongo_client.py` file.\n\n[code-reference:5949549a-9926-11e9-90d1-787b8ab80c39]\n\nThe last part references the documentation database that we want to use (reason why our saved document are in this collection).\n\nAn example of the document model, can be found in `mongo/models.py` (add all models for mongo here). \n\n[code-reference:fb701f10-9926-11e9-a600-787b8ab80c39]\n\nThe important line describing the collection name is referenced here:\n\n[code-reference:27ebee52-9927-11e9-aa5e-787b8ab80c39]\n\nIt is important that each new document object contains the following:\n\n- a `to_json()` function, turning the oject into json for insertion\n\n[code-reference:6c2100d0-9927-11e9-b37c-787b8ab80c39]\n\n- a `from_json()` function, turning json back to an object when doing search queries and recovering objects from mongo\n\n[code-reference:988ee740-9927-11e9-bd0a-787b8ab80c39]\n\n### Nested documents\n\nA small note on nested objects. A Mongo object can contain nested objects. As in Mongo, the concept of join is not used, we nest objects together.\n\nIn our case, a **Document** object can have multiple **FileReference** as a document can contain multiple code references. This is why we have a nested class in `Document` called `File Reference` (which has like every object a `fron_json()` and `to_json` method)\n\n[code-reference:2c863390-9928-11e9-9717-787b8ab80c39]", "refs" : [ { "id" : "5949549a-9926-11e9-90d1-787b8ab80c39", "repo" : "saturnin13/tech-company-documentation", "path" : "backend/mongo/mongo_client.py", "start_line" : 1, "end_line" : 9 }, { "ref_id" : "fb701f10-9926-11e9-a600-787b8ab80c39", "repo" : "saturnin13/tech-company-documentation", "path" : "backend/mongo/models.py", "start_line" : 1, "end_line" : 78 }, { "ref_id" : "27ebee52-9927-11e9-aa5e-787b8ab80c39", "repo" : "saturnin13/tech-company-documentation", "path" : "backend/mongo/models.py", "start_line" : 9, "end_line" : 9 }, { "ref_id" : "6c2100d0-9927-11e9-b37c-787b8ab80c39", "repo" : "saturnin13/tech-company-documentation", "path" : "backend/mongo/models.py", "start_line" : 47, "end_line" : 48 }, { "ref_id" : "988ee740-9927-11e9-bd0a-787b8ab80c39", "repo" : "saturnin13/tech-company-documentation", "path" : "backend/mongo/models.py", "start_line" : 50, "end_line" : 63 }, { "ref_id" : "2c863390-9928-11e9-9717-787b8ab80c39", "repo" : "saturnin13/tech-company-documentation", "path" : "backend/mongo/models.py", "start_line" : 11, "end_line" : 40 } ] })' documentation
mongo --eval 'db.repositories.insert()' documentation