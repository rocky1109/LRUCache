# Cache
Caches are structures for storing data for future use so that it doesn't have to be re-calculated each time it is accessed.

## LRUCache
In LRU cache, when a new input arrives, the resulting output is added to the cache and the oldest output is removed.

## Problem Statement
Implementing a LRU cache which on start-up would load data from file into cache. <br />
The cache can have *N* as its initial size, where it can store *N* elements. <br />
Upon reaching its limit, cache moves the element/record to **cache_file**. <br />
Whereas element which is least recently used will be removed from cache and will be store to **cache_file**. <br />
Further at shutdown, elements of cache are stored into **cache_file** where on start-up its loaded up again. <br />
In general Cache should support CRUD operations as well.

# Solution

For implementing LRUCache, from python collections module **OrderedDict** is one of the data structure which can be used for holding the cache elements. <br />

Advantages:
* Retrieval of element as per key still promises to be of O(1).
* As per LRU, always first element can be used as a candidate for removal.

## class LRUCache
* **file_path**: specifies the path of **cache_file** or **backup_file**.
* **limit**: specifies the limit or size of the cache.
* **unique_identifier**: attribute name of *unique_identifier* in **data object**.
* **record_count**: gives the max. record id available in the system at the time of loading data from **cache_file** into cache.

### insert(*data_object*)
Adds the data into OrderedDict (cache), where, <br />
*key* for OrderedDict is *Unique Identifier*, and value will be the data object itself. <br />
Incase of cache overflow, backup is taken from **cache_file**.

### retrieve(*key*=(optional))
Retrieves the data from OrderedDict (cache), where, <br />
when *key* is not specified, fetches all the elements (of object sorted format), <br />
whereas when *key* is specified, retrieves the particular element. <br />
If element is not found or missing in cache, then element is tried to retrieve from **cache_file**.

### update(*key*, *data_object*)
Updates the data w.r.t *key* in OrderdDict, and replaces it with new *data object*. <br />
*data object*s not available in cache are also supported to be updated in **cache_file**.

### remove(*key*)
Removes the *data object* w.r.t *key*. <br />
*data object* from **cache_files** can also be removed if specified *key* is not available in cache. <br />
Incase of cache underflow, fills the cache space with the element stored in **cache_file**

## Example
**Course** - (course_name, tenure, max_marks). <br />
**Student** records dataset. Student - (first_name, last_name, email, enrolled_courses, marks_scored). <br />
<br />

generate the data from *data_generator.py* as: <br />
```python
>> cd sample
>> python data_generator.py
```

make settings for the cache system in *settings.py*. <br />
* **cache_file**: Path of cache/backup file.
* **cache_limit**: specifies the limit of cache.

further sample usage of LRUCache is implemented in *main.py* <br />
```python
>> python main.py
>> 
```
