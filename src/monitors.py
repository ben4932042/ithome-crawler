from spidermon import Monitor, MonitorSuite, monitors
from src.actions import CloseSpiderAction

@monitors.name('Item count')
class ItemCountMonitor(Monitor):

    @monitors.name('Minimum request url')
    def test_minimum_page_of_process(self):
        item_extracted = getattr(
            self.data.stats, 'response_received_count', 0)
        minimum_threshold = 40

        self.assertTrue(
            item_extracted >= minimum_threshold, msg=f'Ithome iron page crawl less than {minimum_threshold} page'
        )

    @monitors.name('Minimum number of items')
    def test_minimum_number_of_items(self):
        item_extracted = getattr(
            self.data.stats, 'item_scraped_count', 0)
        minimum_threshold = 300

        self.assertTrue(
            item_extracted >= minimum_threshold, msg=f'Extracted less than {minimum_threshold} items'
        )

class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ItemCountMonitor,
    ]

    monitors_failed_actions = [
      CloseSpiderAction
    ]
