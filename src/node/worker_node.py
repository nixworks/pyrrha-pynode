from abc import *

from .node_actions import *


class WorkerNodeDelegate(metaclass=ABCMeta):
    @abstractmethod
    def create_cognitive_job(self, address: str):
        pass

    @abstractmethod
    def start_validating(self, node):
        pass

    @abstractmethod
    def start_computing(self, node):
        pass


class WorkerNode(NodeActions):

    # States

    OFFLINE = 1
    IDLE = 2
    ASSIGNED = 3
    READY_FOR_DATA_VALIDATION = 4
    VALIDATING_DATA = 5
    READY_FOR_COMPUTING = 6
    COMPUTING = 7
    INSUFFICIENT_STAKE = 8
    UNDER_PENALTY = 9

    def __init__(self, delegate: WorkerNodeDelegate, *args, **kwargs):

        self.delegate = delegate

        # State table
        table = {
            self.UNINITIALIZED: StateTableEntry('Uninitialized',
                                                transits_to=[self.IDLE, self.OFFLINE, self.INSUFFICIENT_STAKE],
                                                on_enter=self.on_enter_state_uninitialized,
                                                on_exit=self.on_exit_state_uninitialized),
            self.DESTROYED: StateTableEntry('Destroyed',
                                            transits_to=[],
                                            on_enter=self.on_enter_state_destroyed,
                                            on_exit=self.on_exit_state_destroyed),

            self.OFFLINE: StateTableEntry('Offline',
                                          transits_to=[self.IDLE],
                                          on_enter=self.on_enter_state_offline,
                                          on_exit=self.on_exit_state_offline),
            self.IDLE: StateTableEntry('Idle',
                                       transits_to=[self.OFFLINE, self.ASSIGNED,
                                                    self.UNDER_PENALTY, self.DESTROYED],
                                       on_enter=self.on_enter_state_idle,
                                       on_exit=self.on_exit_state_idle),
            self.ASSIGNED: StateTableEntry('Assigned',
                                           transits_to=[self.OFFLINE, self.READY_FOR_DATA_VALIDATION,
                                                        self.UNDER_PENALTY],
                                           on_enter=self.on_enter_state_assigned,
                                           on_exit=self.on_exit_state_assigned),
            self.READY_FOR_DATA_VALIDATION: StateTableEntry('ReadyForDataValidation',
                                                            transits_to=[self.OFFLINE, self.VALIDATING_DATA, self.IDLE,
                                                                         self.UNDER_PENALTY],
                                                            on_enter=self.on_enter_state_rfdv,
                                                            on_exit=self.on_exit_state_rfdv),
            self.VALIDATING_DATA: StateTableEntry('ValidatingData',
                                                  transits_to=[self.OFFLINE, self.IDLE, self.READY_FOR_COMPUTING,
                                                               self.UNDER_PENALTY],
                                                  on_enter=self.on_enter_state_validating_data,
                                                  on_exit=self.on_exit_state_validating_data),
            self.READY_FOR_COMPUTING: StateTableEntry('ReadyForComputing',
                                                      transits_to=[self.OFFLINE, self.IDLE, self.COMPUTING,
                                                                   self.UNDER_PENALTY],
                                                      on_enter=self.on_enter_state_ready_for_computing,
                                                      on_exit=self.on_exit_state_ready_for_computing),
            self.COMPUTING: StateTableEntry('Computing',
                                            transits_to=[self.OFFLINE, self.IDLE, self.UNDER_PENALTY],
                                            on_enter=self.on_enter_state_computing,
                                            on_exit=self.on_exit_state_computing),
            self.INSUFFICIENT_STAKE: StateTableEntry('InsufficientStake',
                                                     transits_to=[self.OFFLINE, self.IDLE, self.DESTROYED],
                                                     on_enter=self.on_enter_state_insufficient_stake,
                                                     on_exit=self.on_exit_state_insufficient_stake),
            self.UNDER_PENALTY: StateTableEntry('UnderPenalty',
                                                transits_to=[self.OFFLINE, self.IDLE, self.INSUFFICIENT_STAKE],
                                                on_enter=self.on_enter_state_under_penalty,
                                                on_exit=self.on_exit_state_under_penalty),
        }
        super().__init__(table=table, *args, **kwargs)

    def join(self):
        self.event_filter.join()

    def on_enter_state_uninitialized(self, from_state: int):
        pass

    def on_exit_state_uninitialized(self, to_state: int):
        pass

    def on_enter_state_destroyed(self, from_state: int):
        pass

    def on_exit_state_destroyed(self, to_state: int):
        pass

    def on_enter_state_offline(self, from_state: int):
        self.transact_alive()

    def on_exit_state_offline(self, to_state: int):
        pass

    def on_enter_state_idle(self, from_state: int):
        pass

    def on_exit_state_idle(self, to_state: int):
        pass

    def on_enter_state_assigned(self, from_state: int):
        self.delegate.create_cognitive_job(self.cognitive_job_address())
        self.transact_accept_assignment()

    def on_exit_state_assigned(self, to_state: int):
        pass

    def on_enter_state_rfdv(self, from_state: int):
        self.transact_process_to_data_validation()

    def on_exit_state_rfdv(self, to_state: int):
        pass

    def on_enter_state_validating_data(self, from_state: int):
        self.delegate.start_validating(self)

    def on_exit_state_validating_data(self, to_state: int):
        pass

    def on_enter_state_ready_for_computing(self, from_state: int):
        self.transact_process_to_cognition()

    def on_exit_state_ready_for_computing(self, to_state: int):
        pass

    def on_enter_state_computing(self, from_state: int):
        self.delegate.start_computing(self)

    def on_exit_state_computing(self, to_state: int):
        pass

    def on_enter_state_insufficient_stake(self, from_state: int):
        pass

    def on_exit_state_insufficient_stake(self, from_state: int):
        pass

    def on_enter_state_under_penalty(self, from_state: int):
        pass

    def on_exit_state_under_penalty(self, from_state: int):
        pass
