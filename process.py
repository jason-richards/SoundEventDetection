import os
import sys
import timeit
from pydub import AudioSegment
from optparse import OptionParser
from pyaudioclassification import feature_extraction, train, predict, print_leaderboard
from pyaudioclassification.feat_extract import parse_audio_files, parse_audio_file
import numpy as np


DEFAULT_ESC50_DIR     = "./ESC-50"
                        DEFAULT_INDEX             = 100
                                DEFAULT_EPOCHS            = 9752 # Achieves around 98% accuracy


                                        def wav2ogg(wfn, ofn):
                                            """ Work around an issue where pyAudioClassification is
                                            Unable to process input WAV files.
                                            """
                                            print(wfn, " --> ", ofn)
                                            x = AudioSegment.from_file(wfn)
                                                    x.export(ofn, format='ogg')


                                                    def processDB(esc50_dir, output_dir):
                                                    """    This method prepares a new directory formatting
                                                    the ESC-50 database into a format that pyAudioClassification
                                                    Can read.
                                                    """
                                                    AUDIO_SUBDIR         = "%s/audio" % esc50_dir
                                                            METADATA_SUBDIR = "%s/meta"  % esc50_dir

# Obtain the feature labels from the ESC-50 metadata file
#        filename,fold,target,category,esc10,src_file,tak
#            EG:    1-100032-A-0.wav,1,0,dog,True,100032,A
#
                                                                with open(os.path.join(METADATA_SUBDIR, 'esc50.csv')) as i:
                                                                    print(i.readline()) # Skip Header Line
                                                                    for l in i.readlines():
                                                                try:
                                                                            filename, fold, target, category, esc10, src_file, tak = l.split(',')

                                                                                    pathname = os.path.join(output_dir, "%i - %s" % (DEFAULT_INDEX+int(target), category.replace('_', ' ').title()))
                                                                                            if not os.path.exists(pathname):
                                                                                                os.mkdir(pathname)

                                                                                                clip = os.path.join(pathname, filename.replace('.wav', '.ogg'))
                                                                                                        if not os.path.exists(clip):
                                                                                                            wav2ogg(os.path.join(AUDIO_SUBDIR, filename), clip)

                                                                                        except Exception as e:
                                                                                                            pass


                                                                                                            def extractFeatures(feature_output, label_output, output_dir):
                                                                                                            features, labels = None, None
                                                                                                                    if np.DataSource().exists(feature_output) and np.DataSource().exists(label_output):
                                                                                                                        features, labels = np.load(feature_output), np.load(label_output)
                                                                                                        else:
                                                                                                                                    features, labels = feature_extraction(output_dir)
                                                                                                                                            np.save(f, features)
                                                                                                                                            np.save(l, labels)

                                                                                                                                            return features, labels


                                                                                                                                                    def trainModel(features, labels, model_file):
                                                                                                                                                    model = None
                                                                                                                                                            if np.DataSource().exists(model_file):
                                                                                                                                                                from keras.models import load_model
                                                                                                                                                                model = load_model(model_file)
                                                                                                                                        else:
                                                                                                                                                                            model = train(features, labels, epochs=DEFAULT_EPOCHS)
                                                                                                                                                                                    model.save(model_file)

                                                                                                                                                                                    return model


                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                                                            parser = OptionParser()

                                                                                                                                                                                                        parser.add_option("-e", "--esc50",  dest="esc50_dir",  default=DEFAULT_ESC50_DIR, help="Location of ESC-50 database.")
                                                                                                                                                                                                        parser.add_option("-o", "--output", dest="output",          default="./data/",                    help="Output directory.")
                                                                                                                                                                                                        parser.add_option("-m", "--model",  dest="model",             default="./model.h5",            help="Default Model file.")
                                                                                                                                                                                                        parser.add_option("-f", "--feature",dest="feature",         default="./feat.npy",              help="Default Features file.")
                                                                                                                                                                                                        parser.add_option("-l", "--label",    dest="label",             default="./label.npy",            help="Default Label file.")

                                                                                                                                                                                                        (options, args) = parser.parse_args()

                                                                                                                                                                                                                start = timeit.default_timer()
                                                                                                                                                                                                                        processDB(options.esc50_dir, options.output)
                                                                                                                                                                                                                        end = timeit.default_timer()
                                                                                                                                                                                                                                processDBTime = end - start;

start = timeit.default_timer()
        (features, labels) = extractFeatures(options.feature, options.label, options.output)
                             end = timeit.default_timer()
                                   featureExtractionTime = end - start

                                           start = timeit.default_timer()
                                                   model = trainModel(features, labels, options.model)
                                                           end = timeit.default_timer()
                                                                   modelTrainingTime = end - start

                                                                           print("Summary")
                                                                           print("=======")
                                                                           print("ESC-50 Process Time : ", processDBTime)
                                                                           print("Feature Extraction  : ", featureExtractionTime)
                                                                           print("Training Time       : ", modelTrainingTime)

