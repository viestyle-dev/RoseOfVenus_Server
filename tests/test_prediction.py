from scripts.prediction import prediction, load_data, load_model
from unittest import TestCase


class PredictionTest(TestCase):

    def setUp(self) -> None:
        self.data = load_data('data/Rawdata_20220314_175740_626200.csv')
        self.model = load_model('models/haruka20220317EmotionVisualizerFromRSM')

    def test_prediction(self):
        values = prediction(self.model, self.data)
        values = list(values)
        self.assertEqual(values, [0.6523370718759038, 1.0, 1.0, 0.0, 0.5537286715862122, 0.5318449124543188, 0.43723934511187884])
