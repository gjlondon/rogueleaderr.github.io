Title: Postgres Fuzzy Search Using Trigrams (+/- Django)
Slug: tumblr/postgres-fuzzy-search-using-trigrams-django
Date: 2013-05-16 14:00
Tags: []

<p>When building websites, you&#8217;ll often want users to be able to search for something by name. On <a href="http://www.linernotes.com/" target="_blank">LinerNotes</a>, users can search for bands, albums, genres etc from a search bar that appears on the homepage and in the omnipresent nav bar. And we need a way to match those queries to entities in our Postgres database.</p>
<p>At first, this might seem like a simple problem with a simple solution, especially if you&#8217;re using the ORM; just jam the user input into an ORM filter and retrieve every matching string. But there&#8217;s a problem: if you do</p>
<pre><code>Bands.objects.filter(name="beatles")

</code></pre>

<p></p>
<p>You&#8217;ll probably get nothing back, because the name column in your &#8220;bands&#8221; table probably says &#8220;The Beatles&#8221; and as far as Postgres is concerned if it&#8217;s not exactly the same string, it&#8217;s not a match.</p>
<p><strong>Users are naturally terrible at spelling</strong>, and even if they weren&#8217;t they&#8217;d be bad at guessing exactly how the name is formatted in your database. Of course you can use the LIKE keyword in SQL (or the equivalent &#8216;__contains&#8217; suffix in the ORM) to give yourself a little flexibility and make sure that &#8220;Beatles&#8221; returns &#8220;The Beatles&#8221;. But 1) the LIKE keyword requires you to evaluate a regex against every row in your table, or hope that you&#8217;ve configured your indices to support LIKE (a quick Google doesn&#8217;t tell me whether Django does that by default in the ORM) and 2) what if the user types &#8220;Beetles&#8221;?</p>
<p>Well, then you&#8217;ve got a bit of a problem. No matter how obvious it is to human you that &#8220;beatles&#8221; is close to &#8220;beetles&#8221;[1], to the computer they&#8217;re just two non-identical byte sequences. If you want the computer to understand them as similar you&#8217;re going to have to give it a metric for similarity and a method to make the comparison.</p>
<p>There are a few ways to do that. You can do what I did initially and whip out the power tools, i.e. a dedicated search system like Solr or ElasticSearch. These guys have notions of fuzziness built right in (Solr more automatically than ES). But they&#8217;re designed for full-text indexing of documents (e.g. full web pages) and they&#8217;re rather complex to set up and administer. ES has been enough of a hassle to keep running smoothly that I took the time to see if I could push the search workload to Postgres, and hence this article.</p>
<p>Unless you need to do something real fancy, it&#8217;s probably overkill to use them for just matching names.</p>
<p>Instead, we&#8217;re going to follow <a href="http://www.starrhorne.com/2012/02/15/fuzzy-text-search-in-postgresql.html" target="_blank">Starr Horne&#8217;s advice</a> and use a Postgres EXTENSION that lets us build fuzziness into our query in a fast and fairly simple way. Specifically, we&#8217;re going to use an extension called pg_trgm (i.e. &#8220;Postgres Trigram&#8221;) which gives Postgres a &#8220;similarity&#8221; function that can evaluate how many three-character subsequences (i.e. &#8220;trigrams&#8221;) two strings share. This is actually a pretty good metric for fuzzy matching short strings like names.</p>
<p>To use pg_trgm, you&#8217;ll need to install the &#8220;Postgres Contrib&#8221; package. On ubuntu:</p>
<pre><code>sudo apt-get install postgres-contrib

**WARNING: THIS WILL TRY TO RESTART YOUR DATABASE**

</code></pre>
<p>then pop open psql and install pg_trgm (NB: this only works on Postgres 9.1+; Google for the instructions if you&#8217;re on a lower version.)</p>
<pre><code>psql

CREATE EXTENSION pg_trgm;

\dx # to check it's installed

</code></pre>
<p>Now you can do</p>
<pre><code>SELECT *

FROM types_and_labels_view

WHERE label % 'Mountain Goats'

ORDER BY similarity(label, 'Mountain Goats')

DESC LIMIT 100;

</code></pre>

<p>And out will pop the 100 most similar names. This will still take a long time if your table is large, but we can improve that with a special type of index provided by pg_trgm:</p>
<pre><code>CREATE INDEX labels_trigram_index ON types_and_labels_table USING gist (label gist_trgm_ops);

</code></pre>
<p>or</p>
<pre><code>CREATE INDEX labels_trigram_index ON types_and_labels_table USING gin (label gin_trgm_ops);

</code></pre>
<p>(GIN is slower than GIST to build, but answers queries faster.</p>

<p>That&#8217;ll take a while to build (possibly quite a while), but once it does you should be able to fuzzy search with ease and speed. If you&#8217;re using Django, you will have to drop into writing SQL to use this (until someone, <em>maybe you</em>, writes a Django extension to do this in the ORM.)</p>
<p>And as a frustrating finishing note, my attempt to implement this on LinerNotes was not ultimately succesful. It seems that that index query performance is at least O(n) and with 50 million entities in my database queries take at least 10 seconds. I&#8217;ve read that performance is great up to about 100k records then drops off sharply from there. There are some apparently additional options for improving query performance, but I&#8217;ll be sticking with ElasticSearch for now.</p>
<p>[1] Sorry, Googlebot! Not sorry, Bingbot.</p>
