# EdgeRank

Projekat iz algoritama i strukutra podataka.  
Serijalizovani graf dostupan [ovde](https://edgelord.moma.rs/)


## Korišćeni moduli
- Za čitanje csv fajlova: `pip install pandas`  
- Za matricu susedstva: `pip install numpy`  
- Za non-blocking keyboard input: `pip install pynput`  


## Uputstvo za aplikaciju

- Za navigaciju koristiti strelice i esc tastere
- Za odabir opcije u meniju enter
- Za odbair autofill opcije tab
- Za brže listanje statusa, uz strelice držati shift


## Vreme potrebno za pravljenje grafa

Za original csv dataset na Intel i7-11700F (16 threads) procesoru:

<pre>
Bez uračunavanja prijateljevih sklonosti:                 <b>43.6752s</b>
Sa uračunavanjem prijateljevih sklonosti:                 57.2433s
Sa uračunavanjem sklonosti prijatelja od prijatelja:     442.4552s
</pre>

<pre>
Loading data:
   Statuses:                                               0.0465s
   Friends:                                                0.2351s
   Comments:                                               0.1054s
   Reactions:                                              5.9660s
   Shares:                                                 6.6298s

Adding affinity for:
   Friends:                                                1.5490s
   Comments:                                               0.8740s
   Reactions:                                             13.4176s
   Shares:                                                12.7199s
   Affinity of friends:                                   13.5681s
   Affinity of friends friends:                          385.2119s

Total:  442.4552s
</pre>
