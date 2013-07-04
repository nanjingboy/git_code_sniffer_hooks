<?php
class PHPCS_Sniffs_ControlStructures_ControlSignatureSniff extends Squiz_Sniffs_ControlStructures_ControlSignatureSniff
{
    protected function getPatterns()
    {
        return array(
          'try {EOL...} catch (...) {EOL',
          'do {EOL...} while (...); {EOL',
          'while (...) {EOL',
          'for (...) {EOL',
          'if (...) {EOL',
          'foreach (...) {EOL',
          '} else if (...) {EOL',
          '} elseif (...) {EOL',
          '} else {EOL',
        );

    }
}

?>
