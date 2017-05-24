# this file imports all of the other python functions and runs them, fully populating the entire database.

import create_metadata_csv
import createbadan
import getridofbadan
import create_sequenceinfo
import populate_sqam
import features_csv
import create_mitogeneloc
import create_speciesinfo
import populate_sqam_pt2
import populate_rotated
import add_nuclear_genes


# input email that you want to use to access genbank
email = ''

create_metadata_csv.create_metadata_csv(email)
createbadan.createbadan(email)
getridofbadan.getridofbadan()
create_sequenceinfo.create_sequenceinfo()
features_csv.features_csv(email)
populate_sqam.populate_squam()
create_mitogeneloc.create_mitogeneloc()
create_speciesinfo.create_speciesinfo()
populate_sqam_pt2.populate_squam()
populate_rotated.populate_rotated()
add_nuclear_genes.add_nuclear_genes(email)