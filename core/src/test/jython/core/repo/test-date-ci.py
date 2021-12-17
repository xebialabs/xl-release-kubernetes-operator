from java.util import Date

date = Date()

comment = repository.create(factory.configurationItem("Configuration/repo-comment", "test-v3.DummyComment", {"date": date, "comment": "This is a comment"}))

assertEquals(date, comment.date)

comment2 = repository.read(comment.id)

assertEquals(date, comment2.date)

repository.delete(comment.id)