from quantz.quantz_exception import QuantzException


class OnTargetFitListener:
    def on_target_fit(self, target):
        raise QuantzException('You must implement a OnTargetFitListener')
