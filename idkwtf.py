import pickle
unreads = {'main' : ['oren: hi','Bar: hello']}

with open('/Users/bargolan/PycharmProjects/if/cyberfinal_project/unread.pickle', 'wb') as handle:
    pickle.dump(unreads, handle, protocol=pickle.HIGHEST_PROTOCOL)