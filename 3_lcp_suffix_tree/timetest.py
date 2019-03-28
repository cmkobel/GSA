
import gen_lcp
import t4
import time
import st2




# Time test of sa

if True:
    print('n, s')
    for i in range(1, 1000000, 100):
        t0 = time.time()
        a = gen_lcp.suffixes(t4.t4_genome()[:i])
        t1 = time.time()
        print(i, t1-t0, sep = ', ')



# time test of lcp

if False:
    print('n, s')
    for i in range(1, 1000000, 10000):
    #for i in range(1, 10):
        suffixes = gen_lcp.suffixes('a'*i)
        t0 = time.time()
        a = gen_lcp.lcp(suffixes) # den snyder, hvis der ikke er en variabel?
        t1 = time.time()
        #for j in a: print(j)

        print(i, t1-t0, sep = ', ')



# time test of st
if False:
    print('n, s')
    for i in range(50000, 100000, 10000):
    #for i in range(1, 10):
        # suffixes = gen_lcp.suffixes('a'*i)
        # a = gen_lcp.lcp(suffixes) # den snyder, hvis der ikke er en variabel?
        # #for j in a: print(j)


        st = st2.st2(t4.t4_genome()[:i])
        

        t0 = time.time()
        st.construct_tree()


        t1 = time.time()



        print(i, t1-t0, sep = ', ')



