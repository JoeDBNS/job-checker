import scripts.som as som
import modules.module_xlsx_maker as xm


wb_content = {
    'name': 'job_postings',
    'sheets': []
}

som_worksheet = som.RunScan()
wb_content['sheets'].append(som_worksheet)

xm.BuildXlsxFile(wb_content)