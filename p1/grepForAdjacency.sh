 grep "adjacency" $1 | sed "s/<source>programatically<\/source><source>job.xml<\/source>//g" | sed "s/<value>/\n<value>/g" | sed "s/<property>/\n<property>/g"
