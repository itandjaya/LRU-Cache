## Leetcode #146.
## LRU Cache implementation using simple int32 datatype.
## Complexity O(1). Space O(N).
## Data structure: double linked-list with head & tail nodes, coupled with hash lookup table.

    
NOT_FOUND_RETURN = -1;              ## the return value if key not found in cache.
#NOT_FOUND_RETURN = None;
DEBUG   =   0;


class LinkedListNode:
    
    def __init__(self, val = None, nextNode = None):
        self.value = val;
        self.next = nextNode;
        return;
        
class DoubleLinkedListNode(LinkedListNode):
    
    def __init__(self, key = None, val = None, nextN = None, prevN = None):
        super(DoubleLinkedListNode, self).__init__(val, nextN);
        self.key = key;
        self.prev = prevN;
        return;

class DoubleLinkedList:
    
    def __init__(self):
        self.head   =   DoubleLinkedListNode('HEAD');
        self.tail   =   DoubleLinkedListNode('TAIL');
        
        self.head.next  =   self.tail;
        self.tail.prev  =   self.head;
        
        return;

    def __repr__(self):
        ## String representaion of the double linked list.
        
        ptr =   self.head;
        s   =   ["LL: "];
        
        while ptr:
            s.append(   "{}:{} -- ".format( ptr.key, ptr.value));
            ptr = ptr.next;
            
        s.append("\n");    
        return ''.join(s);
    
    def delete_node(    self, node):
        # Delete node from Linked List. Returns None.
        
        prev_node, next_node    =   node.prev, node.next;
        prev_node.next          =   next_node;
        next_node.prev          =   prev_node;
        
        del node;
        return;

    def delete_first_node(   self):
        # Delete first node in Linked List (least recent). Returns the deleted key, value pair.
        
        node        =   self.head.next;
        key, val    =   node.key, node.value;
        self.delete_node(   node);
        return key, val;
    
    def add_key_value(self, key, value):
        ## Createa new node and add it to the last linked list.
        ## Returns the newly added DoubleLL node (needed to be added to the hash_lookup table).
        
        new_node    =   DoubleLinkedListNode(key = key, val = value);
        self.add_to_last(   new_node);
        return new_node;
    
    def add_to_last(self, node):
        ## Adds node to the last position in the linked list.
        
        if not node:            return None;
        
        tail_prev       =   self.tail.prev;
        tail_prev.next  =   node;
        self.tail.prev  =   node;
        
        node.prev       =   tail_prev;
        node.next       =   self.tail;
        
        return;
    
    def move_to_last(self, node):
        ## Moves node to the last position in the linked list.
        ## Retuns None
        
        if not node:        return;
        
        prev_node, next_node    =   node.prev, node.next;
        prev_node.next          =   next_node;
        next_node.prev          =   prev_node;
        
        self.add_to_last(   node);
        
        return;
        
    def remove_node(self, node):
        ## Remove node from the linked list.
        
        if not node:        return;
        
        prev_node, next_node    =   node.prev, node.next;
        
        prev_node.next  =   next_node;
        next_node.prev  =   prev_node;
        
        del node;        
        return;
    
    


class LRUCache:

    def __init__(self, capacity: int):
        
        self.hash_lookup    =   {};                     ## key : key, value =   DoubleLinkedListNode
        self.linked_list    =   DoubleLinkedList();     ## Double Linked-List to keep the order of the LRU Cache.
        self.MAX_SIZE       =   capacity;               ## Max capacity of the LRU Cache.
        self.curr_size      =   0;                      ## Cache size, used to evict least recently used node if cache is full.
        
        return;        
        
    def __repr__(self):
        ## Return str representation of the cache.
        ##  Used for debugging purposes.
        
        arr_s   =   ['## CACHE ## \n'];
        arr_s.append(  self.linked_list.__repr__());        ## Linked-List representation of Cache.
        
        
        ## Hash representation of cache.
        arr_s.append("HASH: ");
        
        for key, node in self.hash_lookup.items():
            s   =   " {}:{} -- ".format(  key, node.value);
            arr_s.append(s);
            
        arr_s.append("\n");
        
        return ''.join(arr_s);

    def delete_least_recent(self) -> None:
        ## Delete least recently used key:value pair from both hash_lookup and Linked List.
        
        key, val    =   self.linked_list.delete_first_node();   ## Delete from Linked List.        
        del self.hash_lookup[key];                              ## Delete from hash_lookup.
        
        self.curr_size -= 1;                                    ## Reduce current size by 1.        
        return;
    
    def get(self, key: int) -> int:
        ## Returns the value of given key, if found, and move it to last (most recent).
        ## If not found, return NOT_FOUND_RETURN value.
        
        try:
            node    =   self.hash_lookup[key];
            x       =   node.value;
            self.linked_list.move_to_last(  node);
            
        
        except KeyError:        x   =   NOT_FOUND_RETURN;        
        finally:                return x;

    def put(self, key: int, value: int) -> None:
        ## Updates the cache with new key, value pair.

        
        ## if new key already exists, update it with new value, and move it to last. Then, return.        
        if key in self.hash_lookup.keys():
                
            node        =   self.hash_lookup[key];
            node.value  =   value;
            self.linked_list.move_to_last(node);
            return;
        
        ## If key doesn't exists in cache and cache size is full, evict the least recently use item.
        elif self.curr_size   ==  self.MAX_SIZE:

            self.delete_least_recent();     ## delete least recently used item from both Linked List and hash_lookup. 
        
        ## finally, add the new key,value pair to the cache.
        new_node    =   self.linked_list.add_key_value(key, value);
        self.hash_lookup[key]   =   new_node;
        
        self.curr_size += 1;
        
        if DEBUG:   print(self);            ## for debug purposes, printing cache content.    
        return;
    
# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
