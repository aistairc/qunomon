@echo off
docker-compose -f docker-compose.yml -f dc-debug-option.yml up -d
echo �y�����z
echo Docker���Ńf�o�b�O���[�h�Ƃ��ĊJ�n���܂����B
echo VSCode�́uRun(���s)�v����backend��ip�̃f�o�b�O���J�n�����Ă��������B
echo ��: �f�o�b�O�����s���Ȃ�����Abackend��ip�͒�~�����܂܂ɂȂ�܂��B�Е������f�o�b�O����ꍇ�ł��A�����̃f�o�b�O�����s���Ă��������B
echo �y�v���O�����̏I���z
echo `docker-compose down` (��ʓI��docker-compose�R�}���h�Ɠ��l�̃R�}���h�ł��B)