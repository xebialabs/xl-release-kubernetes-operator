package test

import org.apache.commons.io.IOUtils

import java.io.FileOutputStream
import java.util.zip.{ZipEntry, ZipFile}
import scala.io.Source
import scala.jdk.CollectionConverters._

object TestUtils {
  def readFromZip(file: String, path: String): String =
    withZipEntry(file, path) {
      case (zipFile, entry) =>
        Source.fromInputStream(zipFile.getInputStream(entry)).getLines().mkString
    }

  def extractEntry(archivePath: String, entryPath: String, destinationPath: String): Int =
    withZipEntry(archivePath, entryPath) {
      case (zipFile, entry) =>
        val fileOutputStream = new FileOutputStream(destinationPath)
        try {
          IOUtils.copy(zipFile.getInputStream(entry), fileOutputStream)
        } finally {
          fileOutputStream.close()
        }
    }

  def listEntries(filePath: String, entryPath: String): Set[String] =
    withinZipFile(filePath)(
      _.entries()
        .asScala
        .filter(_.getName.startsWith(entryPath))
        .map(_.getName)
        .toSet
    )

  private def withinZipFile[T](path: String)(f: ZipFile => T): T = {
    val zipFile = new ZipFile(path)
    try {
      f(zipFile)
    } finally {
      zipFile.close()
    }
  }

  private def withZipEntry[T](filePath: String, entryPath: String)(f: (ZipFile, ZipEntry) => T): T =
    withinZipFile(filePath) {
      zipFile =>
        val entry = zipFile
          .entries()
          .asScala
          .find(_.getName == entryPath)
          .getOrElse(throw new IllegalStateException(s"Cannot find $entryPath in zip file $filePath"))
        f(zipFile, entry)
    }
}
