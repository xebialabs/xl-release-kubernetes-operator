#
from java.lang.System import getProperty
from java.io import File, FileNotFoundException
from javax.xml.parsers import DocumentBuilderFactory

testSalt = UUID.randomUUID().toString()

tempdir = getProperty('java.io.tmpdir')
if (tempdir.endswith('/') or (tempdir.endswith('\\'))):
    filename = tempdir + testSalt + 'archived-tasks.xml'
else:
    filename = tempdir + getProperty('file.separator') + testSalt + 'archived-tasks.xml'
print filename

repository.exportArchivedTasks(filename)
xmlFile = File(filename)
if xmlFile.exists():
    domBuilder = DocumentBuilderFactory.newInstance().newDocumentBuilder()
    try:
        document = domBuilder.parse(filename)
        element = document.getDocumentElement()
        assertEquals('list', element.getTagName())
        assertTrue(element.hasChildNodes())
        nodeList = element.getElementsByTagName('task')
        assertTrue(nodeList.getLength() >= 4)
        for taskNr in xrange(nodeList.getLength()):
            task = nodeList.item(taskNr)
            assertNotNone(task)
            assertTrue(task.hasChildNodes())
            childTagNames = [task.getChildNodes().item(childNr).getNodeName() for childNr in xrange(task.getChildNodes().getLength())]
            for tagName in [u'description',u'startDate',u'completionDate',u'steps',u'metadata']:
                assertTrue(tagName in childTagNames)
        xmlFile.delete()
    except FileNotFoundException, detail:
        raise Exception("XML file %s could not be found and may therefore not have been generated!" % filename)
    except Exception, detail:
        raise Exception("An error occurred while processing XML file %s with exported tasks; detail: %s" % (filename,detail))
else:
    raise Exception("XML file %s could not be found and may therefore not have been generated!" % filename)
