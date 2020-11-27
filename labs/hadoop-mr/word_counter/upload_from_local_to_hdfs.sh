usage() {
  echo -e "Usage: $0 [-f <format>] [-o <hdfs path>]\n"\
       "where\n"\
       "-f defines format of data to upload\n"\
       "-d defines an hdfs destination path\n"\
       "\n"\
        1>&2
  exit 1
}

while getopts ":f:d:" opt; do
    case "$opt" in
        f)  FORMAT=${OPTARG} ;;
        d)  HDFS_PATH=${OPTARG} ;;
        *)  usage ;;
    esac
done

if [[ -z "$HDFS_PATH" ]];
then
  HDFS_PATH="/bdpc/hadoop_mr/word_count/input"
  hadoop fs -rm -R "$HDFS_PATH"
  hdfs dfs -mkdir -p "$HDFS_PATH"
fi

THIS_FILE=$(readlink -f "$0")
THIS_PATH=$(dirname "$THIS_FILE")
BASE_PATH=$(readlink -f "$THIS_PATH/../")
APP_PATH="$THIS_PATH/word_counter-1.0-jar-with-dependencies.jar"

if [ "${FORMAT}" = 'txt' ]; then
  LOCAL_PATH="${BASE_PATH}/data/word_count/*"
else
  LOCAL_PATH="${BASE_PATH}/data/word_count_gzip/*"
fi

echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
echo "THIS_FILE = $THIS_FILE"
echo "THIS_PATH = $THIS_PATH"
echo "BASE_PATH = $BASE_PATH"
echo "-------------------------------------"
echo "LOCAL_PATH = $LOCAL_PATH"
echo "HDFS_PATH = $HDFS_PATH"
echo "-------------------------------------"


SUBMIT_CMD="hdfs dfs -copyFromLocal ${LOCAL_PATH} ${HDFS_PATH}"
echo "$SUBMIT_CMD"
${SUBMIT_CMD}

echo "<<<<<<<<<<<<<<<<<<  HDFS  <<<<<<<<<<<<<<<<<<<<<"

hdfs dfs -ls ${HDFS_PATH}

echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
