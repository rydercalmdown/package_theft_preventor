import os
import pandas as pd


reviewed_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_reviewed')
gcs_base = 'gs://your_bucket_here'


def get_all_images(dir):
    return [x for x in os.listdir(dir) if x.endswith('.jpg')]

package_images = [os.path.join(gcs_base, 'data_reviewed', 'package', x) for x in get_all_images(os.path.join(reviewed_dir, 'package'))]
nopackage_images = [os.path.join(gcs_base, 'data_reviewed', 'no_package', x) for x in get_all_images(os.path.join(reviewed_dir, 'no_package'))]


package_list = [[x, 'package'] for x in package_images]
nopackage_list = [[x, 'no_package'] for x in nopackage_images]

df = pd.DataFrame(package_list + nopackage_list)
df.to_csv('training_data.csv', index=False, header=None)
