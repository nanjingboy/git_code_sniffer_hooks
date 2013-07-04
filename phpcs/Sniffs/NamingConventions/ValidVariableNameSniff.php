<?php
if (class_exists('PHP_CodeSniffer_Standards_AbstractVariableSniff', true) === false) {
    throw new PHP_CodeSniffer_Exception('Class PHP_CodeSniffer_Standards_AbstractVariableSniff not found');
}

class PHPCS_Sniffs_NamingConventions_ValidVariableNameSniff extends Zend_Sniffs_NamingConventions_ValidVariableNameSniff
{
    protected function processVariable(PHP_CodeSniffer_File $phpcsFile, $stackPtr)
    {
    }

    protected function processMemberVar(PHP_CodeSniffer_File $phpcsFile, $stackPtr)
    {
        $tokens = $phpcsFile->getTokens();
        $varName = ltrim($tokens[$stackPtr]['content'], '$');
        $memberProps = $phpcsFile->getMemberProperties($stackPtr);
        $public = ($memberProps['scope'] === 'public');

        if ($public === true) {
            if (substr($varName, 0, 1) === '_') {
                $error = 'Public member variable "%s" must not contain a leading underscore';
                $data  = array($varName);
                $phpcsFile->addError($error, $stackPtr, 'PublicHasUnderscore', $data);
                return;
            }
        } else {
            if (substr($varName, 0, 1) !== '_') {
                $scope = ucfirst($memberProps['scope']);
                $error = '%s member variable "%s" must contain a leading underscore';
                $data  = array($scope, $varName);
                $phpcsFile->addError($error, $stackPtr, 'PrivateNoUnderscore', $data);
                return;
            }
        }
    }

    protected function processVariableInString(PHP_CodeSniffer_File $phpcsFile, $stackPtr)
    {
    }
}
?>
