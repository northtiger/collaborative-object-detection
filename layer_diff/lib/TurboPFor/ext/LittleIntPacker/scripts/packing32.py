#!/usr/bin/env python

def howmany(bit):
    """ how many values are we going to pack? """
    return 32

def howmanywords(bit):
    return (howmany(bit) * bit + 31)/32

def howmanybytes(bit):
    if(howmany(bit) * bit % 8 <>0): raise "error"
    return (howmany(bit) * bit + 7)/8

print("""
/** code generated by packing32.py starts here **/
""")

print("""typedef void (*packblockfnc)(const uint32_t ** pin, uint8_t ** pw);""")
print("""typedef void (*unpackblockfnc)(const uint8_t ** pw, uint32_t ** pout);""")






def plurial(number):
    if(number <> 1):
        return "s"
    else :
        return ""

print("")
print("static void packblock0(const uint32_t ** pin, uint8_t ** pw) {");
print("  (void)pw;");
print("  *pin += {0}; /* we consumed {0} 32-bit integer{1} */ ".format(howmany(0),plurial(howmany(0))));
print("}");
print("")

for bit in range(1,33):
    print("")
    print("/* we are going to pack {0} {1}-bit values, touching {2} 32-bit words, using {3} bytes */ ".format(howmany(bit),bit,howmanywords(bit),howmanybytes(bit)))
    print("static void packblock{0}(const uint32_t ** pin, uint8_t ** pw) {{".format(bit));
    print("  uint32_t * pw32 = *(uint32_t **) pw;");
    print("  const uint32_t * in = *pin;");
    print("  /* we are going to touch  {0} 32-bit word{1} */ ".format(howmanywords(bit),plurial(howmanywords(bit))));
    for k in range(howmanywords(bit)) :
      print("  uint32_t w{0};".format(k))
    for j in range(howmany(bit)):
      firstword = j * bit / 32
      secondword = (j * bit + bit - 1)/32
      firstshift = (j*bit) % 32
      if( firstword == secondword):
          if(firstshift == 0):
            print("  w{0} = (uint32_t) in[{1}];".format(firstword,j))
          else:
            print("  w{0} |= (uint32_t)  in[{1}] << {2};".format(firstword,j,firstshift))
      else:
          print("  w{0} |= (uint32_t) in[{1}] << {2};".format(firstword,j,firstshift))
          secondshift = 32-firstshift
          print("  w{0} = (uint32_t) in[{1}] >> {2};".format(secondword,j,secondshift))
    for k in range(howmanywords(bit)) :
      print("  pw32[{0}] = w{0};".format(k))
    print("  *pin += {0}; /* we consumed {0} 32-bit integer{1} */ ".format(howmany(bit),plurial(howmany(bit))));
    print("  *pw += {0}; /* we used up {0} output bytes */ ".format(howmanybytes(bit)));
    print("}");
    print("")

print("static void unpackblock0(const uint8_t ** pw, uint32_t ** pout) {");
print("  (void) pw;");
print("  memset(*pout,0,{0});".format(howmany(0)));
print("  *pout += {0}; /* we wrote {0} 32-bit integer{1} */ ".format(howmany(0),plurial(howmany(0))));
print("}");
print("")

for bit in range(1,33):
    print("")
    print("/* we packed {0} {1}-bit values, touching {2} 32-bit words, using {3} bytes */ ".format(howmany(bit),bit,howmanywords(bit),howmanybytes(bit)))
    print("static void unpackblock{0}(const uint8_t ** pw, uint32_t ** pout) {{".format(bit));
    print("  const uint32_t * pw32 = *(const uint32_t **) pw;");
    print("  uint32_t * out = *pout;");
    if(bit < 32): print("  const uint32_t mask = UINT32_C({0});".format((1<<bit)-1));
    maskstr = " & mask "
    if (bit == 32) : maskstr = "" # no need
    print("  /* we are going to access  {0} 32-bit word{1} */ ".format(howmanywords(bit),plurial(howmanywords(bit))));
    for k in range(howmanywords(bit)) :
      print("  uint32_t w{0} = pw32[{0}];".format(k))
    print("  *pw += {0}; /* we used up {0} input bytes */ ".format(howmanybytes(bit)));
    for j in range(howmany(bit)):
      firstword = j * bit / 32
      secondword = (j * bit + bit - 1)/32
      firstshift = (j*bit) % 32
      firstshiftstr = ">> {0} ".format(firstshift)
      if(firstshift == 0):
          firstshiftstr ="" # no need
      if( firstword == secondword):
          if(firstshift + bit == 32):
            print("  out[{0}] = (uint32_t) ( w{1}  {2} );".format(j,firstword,firstshiftstr,firstshift))
          else:
            print("  out[{0}] = (uint32_t)  ( ( w{1} {2}) {3} );".format(j,firstword,firstshiftstr,maskstr))
      else:
          secondshift = (32-firstshift)
          print("  out[{0}] = (uint32_t)  ( ( ( w{1} {2} ) | ( w{3} << {4} ) ) {5} );".format(j,firstword,firstshiftstr, firstword+1,secondshift,maskstr))
    print("  *pout += {0}; /* we wrote {0} 32-bit integer{1} */ ".format(howmany(bit),plurial(howmany(bit))));
    print("}");
    print("")

print("static packblockfnc funcPackArr[] = {")
for bit in range(0,32):
  print("&packblock{0},".format(bit))
print("&packblock32")
print("};")

print("static unpackblockfnc funcUnpackArr[] = {")
for bit in range(0,32):
  print("&unpackblock{0},".format(bit))
print("&unpackblock32")
print("};")
print("/** code generated by packing32.py ends here **/")