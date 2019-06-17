# -*- coding: utf-8 -*-
from Tools.aapt.Resource import ResourceNameRef, ResourceId


class IdAssigner(object):

    def consume(self, context, table):
        for package in table.packages:
            assert package.id, "packages must have manually assigned IDs"
            usedTypeIds = set([1 << 8])
            #  Type ID 0 is invalid, reserve it.
            usedTypeIds.add(0)
            #  Collect used type IDs.
            for atype in package.types:
                usedEntryIds = set([1 << 16])
                nextEntryId = 0
                if atype.id:
                    if atype.id in usedTypeIds:
                        #  This ID is already taken!
                        context.getDiagnostics().error = \
                        "type '" + atype.type + "' in " \
                        "package '" + package.name + "' has " \
                        "duplicate ID " + \
                         hex(type.id)
                        return False
                    #  Mark the type ID as taken.
                    usedTypeIds.add(atype.id)
                #  Collect used entry IDs.
                for entry in atype.entries:
                    if not entry.id: continue
                    #  Mark entry ID as taken.
                    if entry.id in usedEntryIds:
                        #  This ID existed before!
                        nameRef = ResourceNameRef(package.name, atype.type, entry.name)
                        takenId = ResourceId(package.id, atype.id,entry.id)
                        context.getDiagnostics().error = \
                        "resource '" + nameRef.toString() + "' " + \
                        "has duplicate ID '" + \
                        takenId.toString() + "'"
                        return False
                    usedEntryIds.add(entry.id)
                #  Assign unused entry IDs.
                for k, entry in enumerate(atype.entries):
                    if entry.id: continue
                    #  Assign the next available entryID.
                    while nextEntryId == min(usedEntryIds):
                        usedEntryIds.remove(nextEntryId)
                        nextEntryId += 1
                    atype.entries[k] = entry._replace(id=nextEntryId)
                    nextEntryId += 1
            nextTypeId = 0
            #  Assign unused type IDs.
            for atype in package.types:
                if atype.id: continue
                while nextTypeId == min(usedTypeIds):
                    usedTypeIds.remove(nextTypeId)
                    nextTypeId += 1
                atype.id = nextTypeId
                nextTypeId += 1
        return True