from scrapy.exceptions import DropItem
from Extractor.DatabaseLayer.dbfuncs import save_to_database
from Extractor.DatabaseLayer.DatabaseRecord import DatabaseRecord


class ExtractorPipeline:
    """Class to process extracted items and save them to the database."""

    def process_item(self, item, spider):
        """
        Process an extracted item and save it to the database.

        Args:
            item: The extracted item.
            spider: The spider that extracted the item.

        Returns:
            item: The processed item.
        """
        db_row = DatabaseRecord(item)
        db_record = save_to_database(db_row)
        if db_record:
            return item
        else:
            raise DropItem
