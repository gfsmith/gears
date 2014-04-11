from  .. import Point, Line, Arc, Circle, Polyline

class DXFParseException(Exception):
    ''' Simple parse error.'''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class DXFFile:

    filename = None
    warnings = []
    def __init__(self, filename):
        self.filename = filename
        self.header = {}
        self.warnings = []
        self.tables = {}
        self.layers = {}
        self.parse()

    def __str__(self):
        entitycount = 0
        for layer in self.layers:
            try:
                entitycount += len(layer)
            except:
                pass
        return "DXFFile[ layers:%d entities:%d warnings:%d ]" % (len(self.layers), entitycount, len(self.warnings))

    def __repr__(self):
        return str(self)
        
    def parse(self):
        f = open(self.filename, 'r')
        state = 'DEFAULT'

        # If suspend read is TRUE, we don't read a new group from the file
        suspend_read = False
        
        # TEMP STORAGE FOR HEADER PARSING
        header_variable = None
        header_args = []

        # TEMP STORAGE FOR TABLE PARSING
        table_variable = None
        table_entries = []

        # TEMP STORAGE FOR ENTITY PARSING
        entity = None
        vertex = None
        layer = None
        plinecount = 0;
        

        # FSM For Parsing
        while True:

            # The read can be suspended for one state transition
            if not suspend_read:
                group = (f.readline(),f.readline())
                if (not group[0]) or (not group[1]): break
                group = self.interpretGroup(group)
            else:
                suspend_read = False

            #### DEFAULT - OUTISDE OF ANY SECTION, AND AT BEGINNING/END OF FILE ####
            if state == 'DEFAULT':
                if group[0] == 0:
                    if group[1] == 'SECTION':
                        state = 'GOT_SECTION'
                        continue
                    if group[1] == 'EOF':
                        break
                else:
                    raise DXFParseException("Data found outside of SECTION!")

            #### GOT A SECTION, BUT DON'T KNOW WHICH ONE YET (GOT_SECTION) ####
            elif state == 'GOT_SECTION':
                if group[0] == 2:
                    if group[1] == 'HEADER':
                        state = 'HEADER_SECTION'
                        continue
                    elif group[1] == 'TABLES':
                        state = 'TABLES_SECTION'
                        continue
                    elif group[1] == 'BLOCKS':
                        state = 'BLOCKS_SECTION'
                        continue
                    elif group[1] == 'ENTITIES':
                        state = 'ENTITIES_SECTION'
                        continue
                    else:
                        self.warnings.append(DXFParseException("Unknown section %s." % group[1]))
                        state = 'MYSTERY_SECTION'

            #
            #
            #    MYSTERY SECTION
            #
            #
            #### CATCH-ALL CURRENTLY UNIMPLEMENTED SECTION
            elif state == 'MYSTERY_SECTION':
                if group[0] == 0:
                    # Store off remaining variable and end this section
                    if group[1] == 'ENDSEC':
                        state = 'DEFAULT'
                        continue                

            #
            #
            #   HEADERS SECTION
            #
            #
            ### INSIDE THE HEADER SECTION (HEADER_SECTION) ####       
            elif state == 'HEADER_SECTION':

                if group[0] == 0:
                    # Store off remaining variable and end this section
                    if group[1] == 'ENDSEC':
                        state = 'DEFAULT'
                        continue
                elif group[0] == 9:
                    state = 'HEADER_VARIABLE'
                    header_variable = group[1]
                    header_args = []
                else:
                    raise DXFParseException("Non-Variable found in HEADER section: %s" % str(group))

            ### RECIEVED A HEADER VARIABLE: STORING OFF ARGUMENTS ####
            elif state == 'HEADER_VARIABLE':
                # End of section or Next Variable
                if group[0] == 0 or group[0] == 9:
                    suspend_read = True
                    state = 'HEADER_SECTION'
                    self.header[header_variable] = tuple(header_args)
                    continue
                
                # Append anything that's not a var name or an ENDSEC is an argument
                # to whatever variable we happen to be storing
                else:
                    header_args.append(group[1])

            #
            #
            #   TABLES SECTION
            #
            #
            #### IN THE TABLES SECTION, BUT NO TABLES ENCOUNTERED YET ####
            elif state == 'TABLES_SECTION':
                if group[0] == 0:
                    if group[1] == 'ENDSEC':
                        state = 'DEFAULT'
                        continue
                    elif group[1] == 'TABLE':
                        state = 'GOT_TABLE'
                        continue

            #### ENCOUNTERED A TABLE, BUT DON'T KNOW ITS NAME YET ####
            elif state == 'GOT_TABLE':
                if group[0] == 2:
                    table_variable = group[1]
                    table_entries = []
                    state = 'TABLE_ENTRY'
                else:
                    raise DXFParseException("Table does not have valid name! %s" % str(group))

            #### INSIDE A NAMED TABLE, READING OFF ENTRIES ####
            elif state == 'TABLE_ENTRY':
                if group[0] == 0:
                    if group[1] == 'ENDTAB':
                        self.tables[table_variable] = table_entries
                        state = 'TABLES_SECTION'
                else:
                    table_entries.append(group)

            #
            #
            #    BLOCKS SECTION
            #
            #
            #### INSIDE THE BLOCKS SECTION BUT HAVEN'T ENCOUNTERED A BLOCK ####
            elif state == 'BLOCKS_SECTION':
                if group[0] == 0:
                    if group[1] == 'ENDSEC':
                        state = 'DEFAULT'
                        continue

            #
            #
            #    ENTITIES SECTION
            #
            #
            #### INSIDE THE ENTITIES SECTION, BUT HAVEN'T ENCOUNTERED ANY ENTITIES YET
            elif state == 'ENTITIES_SECTION':
                if group[0] == 0:
                    if group[1] == 'ENDSEC':
                        state = 'DEFAULT'
                        continue
                    elif group[1] == 'LINE':
                        state = 'LINE'
                        entity = Line(Point(),Point())
                        continue
                    elif group[1] == 'POINT':
                        state = 'POINT'
                        entity = Point()
                        continue
                    elif group[1] == 'CIRCLE':
                        state = 'CIRCLE'
                        entity = Circle(Point(), 0)
                        continue
                    elif group[1] == 'ARC':
                        state = 'ARC'
                        entity = Arc(Point(), 0, 0, 0, geometry.CCW)
                        continue
                    elif group[1] == 'POLYLINE':
                        state = 'POLYLINE'
                        entity = Polyline()
                        plinecount+=1
                        continue
            # LINE
            elif state == 'LINE':
                # Encountered the next entity, or an ENDSEC
                if group[0] == 0:
                    self.createLayerifMissing(layer)
                    self.layers[layer].append(entity)
                    suspend_read = True
                    state = 'ENTITIES_SECTION'
                    continue
                # A and B coordinates
                elif group[0] == 10:
                    entity.a.x = group[1]
                elif group[0] == 20:
                    entity.a.y = group[1]
                elif group[0] == 11:
                    entity.b.x = group[1]
                elif group[0] == 21:
                    entity.b.y = group[1]
                elif group[0] == 30 or group[0] == 31:
                    pass # Z COORDINATES ARE IGNORED: 2D DXF ONLY

                # Layer name
                elif group[0] == 8:
                    layer = group[1]
                else: pass

            # POINT
            elif state == 'POINT':
                if group[0] == 0:
                    self.createLayerifMissing(layer)
                    self.layers[layer].append(entity)
                    suspend_read = True
                    state = 'ENTITIES_SECTION'
                    continue
                elif group[0] == 10:
                    entity.x = group[1]
                elif group[0] == 20:
                    entity.y = group[1]
                elif group[0] == 30:
                    pass # Z COORDINATES ARE IGNORED: 2D DXF ONLY
                elif group[0] == 8:
                    layer = group[1]
                else:pass
                
            # CIRCLE
            elif state == 'CIRCLE':
                # Encountered the next entity, or an ENDSEC
                if group[0] == 0:
                    self.createLayerifMissing(layer)
                    self.layers[layer].append(entity)
                    suspend_read = True
                    state = 'ENTITIES_SECTION'
                    continue
                # A and B coordinates
                elif group[0] == 10:
                    entity.center.x = group[1]
                elif group[0] == 20:
                    entity.center.y = group[1]
                elif group[0] == 30:
                    pass # Z COORDINATES ARE IGNORED: 2D DXF ONLY
                elif group[0] == 40:
                    entity.radius = group[1]
                # Layer name
                elif group[0] == 8:
                    layer = group[1]
                else: pass

            # ARC
            elif state == 'ARC':
                from math import pi
                # Encountered the next entity, or an ENDSEC
                if group[0] == 0:
                    self.createLayerifMissing(layer)
                    self.layers[layer].append(entity)
                    suspend_read = True
                    state = 'ENTITIES_SECTION'
                    continue
                # A and B coordinates
                elif group[0] == 10:
                    entity.center.x = group[1]
                elif group[0] == 20:
                    entity.center.y = group[1]
                elif group[0] == 30:
                    pass # Z COORDINATES ARE IGNORED: 2D DXF ONLY
                elif group[0] == 40:
                    entity.radius = group[1]
                elif group[0] == 50:
                    entity.startangle = group[1]*pi/180.0   # Angles are stored as RADIANS
                elif group[0] == 51:
                    entity.endangle = group[1]*pi/180
                # Layer name
                elif group[0] == 8:
                    layer = group[1]
                else: pass

            # POLYLINE
            elif state == 'POLYLINE':
                if group[0] == 0:
                    if group[1] == 'VERTEX':
                        vertex = Point()
                        state = 'VERTEX'
                        continue
                    else:
                        self.createLayerifMissing(layer)
                        self.layers[layer].append(entity)
                        state = 'ENTITIES_SECTION'
                        continue
                elif group[0] == 70:
                    flags = group[1]
                    if flags & 0x01:
                        pass
                        #entity.

            elif state == 'VERTEX':
                if group[0] == 0:
                        entity.appendPoint(vertex)
                        suspend_read = True
                        state = 'POLYLINE'
                        continue
                elif group[0] == 10:
                    vertex.x = group[1]
                elif group[0] == 20:
                    vertex.y = group[1]
                    
            else:
                f.close()
                raise DXFParseException("I've entered an unknown state: %s" % state)
        f.close()

    def createLayerifMissing(self, layer):
        '''
        Creates a named layer for this DXFFile if none exists.
        If one exists, it is left alone.
        '''
        try: self.layers[layer]
        except: self.layers[layer] = []

        
    def interpretGroup(self,group):
        '''
        Accepts a group tuple, and returns the same tuple with
        the second value cast to the appropriate type, based on the
        group code.  Raises a DXFParseException for invalid group codes
        or un-parseable group data.
        LIFTED DIRECTLY FROM DXF SPEC:
        http://www.dcs.ed.ac.uk/home/mxr/gfx/3d/DXF12.spec
        '''
        group = (int(group[0].strip()), group[1].strip())
        if group[0] <= 9:                            # String
            return (group[0],group[1])
        elif group[0] <= 59:                        # Floating point
            return (group[0],float(group[1]))
        elif group[0] <= 79:                        # Integer
            return (group[0], int(group[1]))
        elif group[0] >= 140 and group[0] <= 147:   # Floating point
            return (group[0], float(group[1]))
        elif group[0] >= 170 and group[0] <= 175:   # Integer
            return (group[0], int(group[1]))
        elif group[0] >= 210 and group[0] <= 239:   # Floating point
            return (group[0], float(group[1]))
        elif group[0] == 999:                       # Comment (String)
            return (group[0], str(group[1]))        
        elif group[0] >= 1010 and group[0] <= 1059: # Floating Point
            return (group[0],float(group[1]))
        elif group[0] >= 1060 and group[0] <= 1079: # Integer
            return (group[0], int(group[1]))
        elif group[0] >= 1000 and group[1] <= 1009: # String
            return (group[0], str(group[1]))
        else:
            ## Try to recover from an unidentified group code
            self.warnings.append(DXFParseException("Undefined group code %d" % group[0]))
            try:
                return (group[0], int(group[1]))
            except:
                try:
                        return (group[0], float(group[1]))
                except:
                        return (group[0], group[1])
        

if __name__ == '__main__':
    
    d = DXFFile('sample.dxf')
    print d
    print d.layers.keys()
    for layer in d.layers:
        print d.layers[layer]
