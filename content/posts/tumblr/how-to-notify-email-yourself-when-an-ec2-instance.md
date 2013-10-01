Title: How to notify/email yourself when an EC2 instance terminates
Slug: tumblr/how-to-notify-email-yourself-when-an-ec2-instance
Date: 2013-04-24 20:23
Tags: []

<p>I make pretty heavy use of EC2 spot instances, which as you know can terminate at any time with no warning.</p>
<p>In order to get my spots back up ASAP, I&#8217;d like be notified when they terminate.</p>
<p>This turned out to be much harder than I expected. I thought I&#8217;d be able to add a simple script that would send me an email when the instance shuts down (Amazon is nice enough to send a shutdown command on termination instead of just pulling the plug.)</p>
<p>But that approach has a couple of problems.</p>
<p>First, you can&#8217;t easily send email from EC2 instances (because of spammers) and have to manually get instances whitelisted by elastic IP <em>which is a pain</em>.</p>
<p>Second, it&#8217;s not the easiest thing to write a shutdown hook in Linux.</p>
<p>So, here&#8217;s a solution for both of those problems.</p>
<p><strong>The email problem</strong></p>
<p>Amazon has a service called CloudWatch that seems great for this, except that it can only monitor metrics <em>emitted by running instances</em>. So you can&#8217;t set it to alert you on a system shutdown, nor on a metric polling failure because it randomly misses packets all the time.</p>
<p>So the solution is a different Amazon service called SNS (simple notification service) that will let you <em>trigger an event</em> that can be configured to send you an email. So we&#8217;re going to write a script that tells SNS to send us an email.</p>
<p>(SNS is free for ~200k requests/month, so unless you&#8217;re planning on doing something nuts this approach should have no marginal costs.)</p>
<p>To do that, you first need to set up a &#8220;topic&#8221; in SNS. Go to the <a href="https://console.aws.amazon.com/sns/home?region=us-east-1#s=TopicDetails" target="_blank">SNS dashboard</a> and</p>
<p>1) click &#8220;create topic&#8221;.<br/> 2) Create a topic called &#8220;instance_down&#8221; or whatever you like.<br/> 3) Click the topic and click &#8220;create subscription&#8221;<br/> 4) Choose protocol &#8220;email&#8221; and enter your email address as the endpoint</p>
<p>To use SNS in a script, we need the <a href="http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html" target="_blank">AWS command line tools</a>.</p>
<p>If you already have pip installed, just</p>
<blockquote>
<p>pip install awscli</p>
</blockquote>
<p>Then:</p>
<blockquote>
<p>touch ~/.awsconfig<br/> emacs ~/.awsconfig</p>
</blockquote>
<p>Make it say:</p>
<blockquote>
<p>[default]<br/> AWS_ACCESS_KEY_ID=&#171;&#160;YOUR AWS ID&#187;<br/> AWS_SECRET_ACCESS_KEY=&#171;&#160;YOUR AWS SECRET KEY&#187;<br/> region=&#171;&#160;YOUR REGION&#160;&#187;</p>
</blockquote>
<p>Create an init.d script:</p>
<blockquote>
<p>sudo emacs /etc/init.d/ec2-shutdown</p>
</blockquote>
<p>Make it say:</p>
<blockquote>
<p>#! /bin/sh<br/> ### BEGIN INIT INFO<br/> # Provides: ec2-terminate<br/> # Required-Start: $network $syslog<br/> # Required-Stop:<br/> # Default-Start:<br/> # Default-Stop:<br/> # Short-Description: restart<br/> # Description: send termination email<br/> ### END INIT INFO<br/> #</p>
<p>export AWS_CONFIG_FILE={{ YOUR CONFIG FILE }}<br/> export AWS_DEFAULT_REGION={{ YOUR REGION }} # config file not picking up region for some reason<br/> sudo -E aws sns publish &#8212;topic-arn {{ YOUR SNS ARN }} &#8212;message &#8220;ec2 ser\<br/> ver {{ YOUR IDENTIFIER }} went down at $(date)&#8221;<br/> sleep 3 # make sure the message has time to send</p>
<p>exit 0</p>
</blockquote>
<p>That script will tell SNS to send you a email saying your server is down and giving the time. You can customize the message however you like.</p>
<p><strong>The Shutdown Script Problem</strong></p>
<p>So how do we make this run on shutdown?</p>
<p>We&#8217;re going to use init.d scripts. It&#8217;s taken me a little while to get my head around how this works, but in a nutshell&#8230;</p>
<p>Linux has a concept of &#8220;runstates&#8221;, which include things like &#8220;shutdown&#8221; and &#8220;logged in&#8221;. You can tell Ubuntu to run shell scripts when it changes into a runstate by placing scripts in certain folders in side of /etc. The two states that concern us are rc0 and rc6, i.e. &#8220;shutdown&#8221; and &#8220;reboot&#8221;, which correspond to folders /etc/rc0.d and /etc/rc6.d respectively.</p>
<p>Ubuntu has a command line tool, update-rc.d that will automatically symlink scripts into the appropriate folders depending on the CL paramaters you pass it. It&#8217;s all a bit complicated, but all you need to do here is:</p>
<blockquote>
<p>sudo update-rc.d ec2-shutdown start 10&#160;0 6 .</p>
</blockquote>
<p>(This says run the script on entering run states 0 and 6, shutdown and reboot. And put it 10th in the list of things to do)</p>
<p>And that should do it! Now your instance should send you an email whenever it shuts down, terminates or reboots. I&#8217;m not sure how limit to just EC2 termination, but please comment if you know!</p>
<p>If you have any problems, leave a comment.</p>
<p>And if you find this useful, consider <a href="https://twitter.com/rogueleaderr" target="_blank">following me on Twitter</a>.</p>
