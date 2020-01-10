"""
BERT Pipeline
"""
import spacy
from medacy.pipelines.base.base_pipeline import BasePipeline
from medacy.pipeline_components import BertLearner
from medacy.pipeline_components import TextExtractor
from medacy.pipeline_components import SystematicReviewTokenizer

class BertPipeline(BasePipeline):
    """
    A pipeline for clinical named entity recognition. A special tokenizer that breaks down a
    clinical document to character level tokens defines this pipeline.
    """

    def __init__(self, entities, **kwargs):
        """
        Create a pipeline with the name 'bert_pipeline' utilizing
        by default spaCy's small english model.

        :param entities: Possible entities.
        :param cuda_device: Which cuda device to use. -1 for CPU.
        :param batch_size: Batch size to use during training.
        :param learning_rate: Learning rate to use during training.
        :param epochs: Number of epochs to use for training.
        """
        description = ('Pipeline tuned for the extraction of ADE related entities from the 2018',
                       'N2C2 Shared Task')
        super().__init__(entities=entities, spacy_pipeline=spacy.load("en_core_web_sm"))

        self.cuda_device = kwargs['cuda_device']
        self.batch_size = kwargs['batch_size'] if kwargs['batch_size'] else 8
        self.learning_rate = kwargs['learning_rate'] if kwargs['learning_rate'] else 1e-5
        self.epochs = kwargs['epochs'] if kwargs['epochs'] else 3
        self.pretrained_model = kwargs['pretrained_model']
        self.using_crf = kwargs['using_crf']

    def get_learner(self):
        """Get the learner object for this pipeline.

        :return: BertLearner.
        """
        learner = BertLearner(
            self.cuda_device,
            pretrained_model=self.pretrained_model,
            batch_size=self.batch_size,
            learning_rate=self.learning_rate,
            epochs=self.epochs,
            using_crf=self.using_crf
        )
        return ('BERT', learner)

    def get_tokenizer(self):
        """Get tokenizer for this pipeline.

        :return: Systematic review tokenizer.
        """
        tokenizer = SystematicReviewTokenizer(self.spacy_pipeline)
        return tokenizer

    def get_feature_extractor(self):
        """Get feature extractor for this pipeline.

        :return: Text only extractor.
        """
        extractor = TextExtractor()
        return extractor