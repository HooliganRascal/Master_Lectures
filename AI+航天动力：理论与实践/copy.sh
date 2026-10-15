rsync -avh --progress \
    -e "ssh -p 2205" \
    --exclude='processor*/' \
    /home/mteltn/Desktop/Master/Lectures/AI+航天动力：理论与实践/ \
	try@10.69.140.82:~/workPath/hxn/Notebooks/ \
# 	rbcc@10.69.140.82:/media/rbcc/新加卷1/HXN/Notebooks/ \
#	try: 2205, rbcc:2234
