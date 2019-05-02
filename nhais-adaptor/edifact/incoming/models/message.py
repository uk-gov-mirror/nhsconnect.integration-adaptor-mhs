class MessageSegmentRegistrationDetails(object):
    """
    A representation of the incoming edifact registration details contained in a message
    """

    def __init__(self, transaction_number):
        """
        :param transaction_number: the transaction number from the incoming edifact message. Should match transaction
        number of the outgoing message
        """
        self.transaction_number = transaction_number


class MessageSegmentBeginningDetails(object):
    """
    A representation of the incoming edifact message beginning details contained in a message
    """

    def __init__(self, reference_number):
        """
        :param reference_number: the reference number from the incoming edifact interchange
        will be used to determine if the transaction is approved
        """
        self.reference_number = reference_number


class MessageSegment(object):
    """
    A representation of the incoming edifact message
    """

    def __init__(self, message_beginning, message_registration):
        """
        :param message_beginning: the incoming message beginning section
        :param message_registration: the incoming message registration details
        """
        self.message_beginning = message_beginning
        self.message_registration = message_registration


class Messages(list):
    """
    A collection of all the incoming messages contained within an interchange
    """

    def __init__(self, messages):
        """
        :param messages: a collections of the incoming messages
        """
        self.messages = messages
        super().__init__(messages)
