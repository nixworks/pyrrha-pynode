from eth.stateful_contract import *


class NodeActions(StatefulContract):

    def cognitive_job_address(self) -> str:
        address = self.contract.call().activeJob()
        if address == '0':
            address = None
        return address.lower()

    def transact_alive(self):
        self.logger.info('Sending alive status')
        pass

    def transact_accept_assignment(self):
        self.logger.info('Accepting assignment')
        self.transact('acceptAssignment', lambda tx: tx.acceptAssignment())

    def transact_decline_assignment(self):
        self.logger.info('Declining assignment')
        self.transact('declineAssignment', lambda tx: tx.declineAssignment())

    def transact_process_to_data_validation(self):
        self.logger.info('Processing to data validation')
        self.transact('processToDataValidation', lambda tx: tx.processToDataValidation())

    def transact_accept_valid_data(self):
        self.logger.info('Confirming data validness')
        self.transact('acceptValidData', lambda tx: tx.acceptValidData())

    def transact_decline_valid_data(self):
        self.logger.info('Confirming data validness but declining task')
        self.transact('declineValidData', lambda tx: tx.declineValidData())

    def transact_report_invalid_data(self):
        self.logger.info('Reporting invalid data')
        self.transact('reportInvalidData', lambda tx: tx.reportInvalidData())

    def transact_process_to_cognition(self):
        self.logger.info('Processing to cognitive work')
        self.transact('processToCognition', lambda tx: tx.processToCognition())

    def transact_provide_results(self, ipfs_file: str):
        self.logger.info('Providing results')
        self.transact('provideResults', lambda tx: tx.provideResults(ipfs_file))
