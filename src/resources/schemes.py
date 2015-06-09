__author__ = 'alisonbnt'

from src.scheme_loader import SchemeLoader

import src.resstatus as _status
import src.resources.hsres as hsres


class SchemesResource(hsres.HomeShellResource):

    def get(self):

        loader = SchemeLoader()
        scheme_rel = loader.scheme_rel

        self.set_status(_status.STATUS_OK)
        self.add_content('schemes', scheme_rel)

        return self.end()
