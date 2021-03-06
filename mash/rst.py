from docutils import core

def rst_to_html_fragment(source):
    parts = core.publish_parts(source=source, writer_name='html')
    return parts['body_pre_docinfo'] + parts['fragment']
