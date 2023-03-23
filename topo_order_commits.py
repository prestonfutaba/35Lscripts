# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.

import os
import sys
import zlib

# borrowed from spec
class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

# 1) Discover .git directory
def get_git_path():
    path = os.getcwd() #set path var to current working dir

    while (path != os.path.dirname(path)): #given certain path, use os.path.dirname(path) to return head of path
        has_git = os.path.isdir("%s/.git" % path) #bool if .git is an existing dir
        if (has_git == True): #searches if .git is an existing dir
            return os.path.join(path, ".git") #if so, we are successful and can exit, returning the path 
        else:
            path = os.path.dirname(path) #else we shorten path and keep looking for .git

    sys.exit("Not inside a Git repository") #failure message

# 2) Get the list of local branch names
def get_branches():

    git_dir = get_git_path() #using our fn to find .git dir, set it to path var
    branch_dir = os.path.join(git_dir, "refs", "heads") #specify branch directory in this var

    branches_list = [] #intialize list of branches
    for root_path, dirs, files in os.walk(branch_dir): #traverse branch path
        for file in files: 
            branch_path = os.path.join(root_path, file) 
            branches_list.append(branch_path[len(branch_dir) + 1:]) #append path of branch into branch array

    branch_hashes = {} #list of branch hashes for each branch
    for branch in branches_list: #pretty much the same idea as above but instead of the path we are looking at branch hashes
        branch_path = os.path.join(branch_dir, branch) 
        branch_hash = open(branch_path, "r").read().replace("\n", "") #read hashes, kind of like decompress
        branch_hashes[branch] = branch_hash

    return branch_hashes

#3) first task: need to get the commit parents before we can build the graph
def get_parents(commit): #takes commit and returns parents of particular commit
    git_path = get_git_path() #our first fn that we made
    path = os.path.join(git_path, "objects", commit[:2], commit[2:]) #makes path with objects and commits, adjusts to right path

    commit_data = zlib.decompress(open(path, "rb").read()) #use zlib to decompress commits, make readable
    is_commit = commit_data[:6] == b"commit"

    parents = [] #intialize list of parent commit(s)
    if is_commit:
        commit_data = commit_data.decode().split("\n") #list split at spaces
        for commit in sorted(commit_data):
            commit_type, commit_message = commit[:6], commit[7:] #6 and 7 correspond to commit type and message
            if(commit_type == "parent"): #we are looking for the parents, so if passes this if we append to parents list
                parents.append(commit_message)

    return parents

#resume here
def create_graph():
    branches = get_branches()

    graph = {}
    for commit in sorted(branches.values()):
        git_path = get_git_path()
        path = os.path.join(git_path, "objects", commit[:2], commit[2:])

        commit_data = zlib.decompress(open(path, "rb").read())
        is_commit = commit_data[:6] == b"commit"

        if is_commit:
            commits_stack = [commit]

            while(commits_stack != []):
                commit = commits_stack.pop()

                if commit in graph:
                    node = graph[commit]
                else:
                    node = CommitNode(commit)

                parents = get_parents(commit)
                for parent in sorted(parents):
                    node.parents.add(parent)

                    if parent in graph:
                        parent_node = graph[parent]
                    else:
                        parent_node = CommitNode(parent)
                        commits_stack.append(parent)

                    parent_node.children.add(commit)
                    graph[parent] = parent_node

                graph[commit] = node

    return graph


def create_topo_order():
    graph = create_graph()
    root_commits = []

    topo_order = []
    visited = set()

    for commit in sorted(graph):
        if len(graph[commit].parents) == 0:
            root_commits.append(commit)

    for root in root_commits:
        if root not in visited:
            commits_stack = [root]

        while (commits_stack != []):
            commit = commits_stack.pop()

            if commit not in visited:
                if len(graph[commit].parents) >= 2:

                    parent_stack = []
                    parent_visited = []

                    for parent in sorted(graph[commit].parents):
                        if parent not in visited:
                            parent_stack = [parent]

                            visited.add(parent)
                            while (parent_stack != []):
                                parent_commit = parent_stack.pop()

                                for parent in sorted(
                                        graph[parent_commit].parents):
                                    if parent not in visited:
                                        parent_stack.append(parent)

                                    parent_visited.append(parent_commit)
                                    visited.add(parent_commit)

                    for node in reversed(parent_visited):
                        topo_order.append(node)

                for child in sorted(graph[commit].children):
                    if child not in visited:
                        commits_stack.append(child)

                topo_order.append(commit)
                visited.add(commit)

    return topo_order


def print_topo_order_graph():
    branches = get_branches()
    graph = create_graph()
    topo_order = create_topo_order()[::-1]

    is_sticky = False
    for i in range(len(topo_order)):
        commit = topo_order[i]
        node = graph[commit]

        if is_sticky:
            is_sticky = False
            sticky_commits = "="

            for child in sorted(node.children):
                sticky_commits += "%s " % child
            print(sticky_commits.rstrip())

        print(commit, end="")

        for branch in sorted(branches.keys()):
            if branches[branch] == commit:
                output = " " + branch
                print(output, end="")

        print()

        if i != len(topo_order) - 1:
            next_node = graph[topo_order[i + 1]]

            if commit not in next_node.children:
                output = ""

                for parent in sorted(node.parents):
                    output += "%s " % parent

                print(output.strip() + "=", end="\n\n")
                is_sticky = True


def topo_order_commits():
    return print_topo_order_graph()


if __name__ == "__main__":
    topo_order_commits()