# -*- coding: utf-8 -*-

import threading
import Queue
import functools
import inspect

import network
import CustomRegEx

# Message identifier
PROCESS_START  = 'start'
PROCESS_END    = 'end'
PROCESS_CANCEL = 'cancel'
PROCESS_ERROR  = 'error'
PROCESS_PAUSE  = 'pause'
PROCESS_MESSAGE = 'message'
PROCESS_DATA   = 'data'


def parsingUrlData(url, regexPattern, initConf=None, **kwargs):
    yield [PROCESS_MESSAGE, ('Contactando sitio web bvc',), kwargs]
    if not initConf:
        initConf = r'curl  --user-agent "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36" --cookie-jar "cookies.lwp" --location'
    net = network.network(initConf)
    content, end_url = net.openUrl(url)
    yield [PROCESS_MESSAGE, ('Pagina weg entregada',), kwargs]

    reg = CustomRegEx.compile(regexPattern)

    k = 0
    pos = baseIndex = 0
    while True:
        match = reg.search(content, pos)
        if not match:
            break
        k += 1
        pos = match.end(0)
        yield [PROCESS_DATA, (k, match, baseIndex), kwargs]

class threadManager:
    def __init__(self, guiOwner=None, numWorkers=1):
        """

        :param  guiOwner: Instance of a Tkinter class.
        :param  numWorkers: Number of threads operating simultaneously
        :param  messageSystemListener: Function to follow the system steps
                in executing the process. See processMessage to see the
                input data.
        """
        if guiOwner:
            assert hasattr(guiOwner, 'after'), 'guiOwner must be a Tkinter widget'
            self.syncQueue = Queue.Queue()
        self.guiOwner = guiOwner
        self.lock = threading.Lock()
        self.mutex = threading.Event()
        self.asyncQueue = Queue.Queue()
        self.waitingList = []
        self.activeList = {}
        self.preActiveList = []
        self.syncProcess = []
        self.counter = 0
        self.numWorkers = numWorkers
        self.activeWorkers = 0

    def startAsyncThreads(self):
        delta = self.numWorkers - self.activeWorkers
        for k in range(delta):
            t = threading.Thread(target=self.asyncWorker)
            t.daemon = True
            t.start()
            self.activeWorkers += 1

    def syncWorker(self, endFlag):
        queue = self.syncQueue
        nProcess = 100
        while nProcess and not queue.empty():
            dataType, processTag, queueProcessor, args, kwargs =  queue.get()
            # if processTag in self.syncProcess:
            if dataType == PROCESS_DATA and processTag in self.syncProcess:
                try:
                    queueProcessor(dataType, processTag, *args, **kwargs)
                except Exception as e:
                    dataType = PROCESS_ERROR
                    queueProcessor(dataType, processTag, Exception('Error executing %s' % queueProcessor.__name__), **kwargs)
                    queueProcessor(dataType, processTag, e, **kwargs)
                    queueProcessor(PROCESS_MESSAGE, processTag, 'Waiting for the %s Process to be canceled ' % processTag, **kwargs)
                    if processTag in self.activeList:
                        cancel_event = self.activeList[processTag][0]
                        cancel_event.clear()
            elif dataType == PROCESS_START:
                self.syncProcess.append(processTag)
                queueProcessor(PROCESS_START, processTag, 'Inicio de proceso', **kwargs)
            elif dataType == PROCESS_END:
                queueProcessor(PROCESS_END, processTag, *args, **kwargs)
            elif dataType == PROCESS_MESSAGE:
                queueProcessor(dataType, processTag, *args, **kwargs)
            elif dataType == PROCESS_ERROR:
                queueProcessor(PROCESS_END, processTag, *args, **kwargs)
            elif dataType == PROCESS_CANCEL:
                queueProcessor(PROCESS_CANCEL, processTag, *args, **kwargs)
            if dataType in [PROCESS_END, PROCESS_CANCEL, PROCESS_ERROR] and processTag in self.syncProcess:
                self.syncProcess.remove(processTag)

            endFlag = len(self.syncProcess) == 0 and len(self.activeList) == 0
            queue.task_done()
            nProcess -= 1
        if not queue.empty() or not endFlag:
            self.guiOwner.after(100, self.syncWorker, endFlag)

    def asyncWorker(self):
        queue = self.asyncQueue
        guiQueue = self.syncQueue
        while self.mutex.is_set():
            item = queue.get()
            dataType, processTag, processDataFunc, args, kwargs, outProcessor = item
            if dataType == PROCESS_DATA:
                """Entrando por aquí se tiene que no se ha iniciado el proceso por lo cual 
                se informa al sistema para setablecer condiciones iniciales como los eventos
                de wait y cancel entre otros"""
                guiQueue.put((PROCESS_START, processTag, outProcessor, ('Inicio proceso',), kwargs))
                self.processEvent(PROCESS_START, processTag, outProcessor, *args, **kwargs)
                try:
                    cancel_event, wait_event = self.activeList[processTag][:2]
                    kwargs['lock'] = self.lock
                    iterator = processDataFunc(*args, **kwargs)
                    if not inspect.isgenerator(iterator):
                        theIterator = iter([iterator, ])
                    while self.mutex.is_set() and cancel_event.is_set():
                        dataType, args, kwargs = iterator.next()
                        wait_event.wait()
                        guiQueue.put((dataType, processTag, outProcessor, args, kwargs))
                except StopIteration:
                    eventType = PROCESS_END
                    guiQueue.put((PROCESS_END, processTag, outProcessor, ('Finaliza proceso',), kwargs))
                except Exception as e:
                    eventType = PROCESS_ERROR
                    guiQueue.put((PROCESS_ERROR, processTag, outProcessor, (e,), kwargs))
                else:
                    eventType = PROCESS_CANCEL
                    cancel_event = self.activeList[processTag][0]
                    if not cancel_event.is_set():
                        if processTag in self.syncProcess:
                            args = ('Proceso cancelado por el usuario',)
                            kwargs = dict(origen=2)
                        else:
                            args = ('Proceso cancelado por el sistema por falla en proceso del usuario',)
                            kwargs = dict(origen=1)
                    elif not self.mutex.is_set():
                        args = ('Proceso cancelado por el sistema',)
                        kwargs = dict(origen=1)
                    guiQueue.put((eventType, processTag, outProcessor, args, kwargs))
                finally:
                    self.processEvent(eventType, processTag, outProcessor, *args, **kwargs)
            queue.task_done()
        self.activeWorkers -= 1

    def processEvent(self, eventType, processTag, outProcessor, *evargs, **evkwargs):
        if eventType == PROCESS_START:
            evkwargs['lock'] = self.lock
            cancel_event, wait_event = threading.Event(), threading.Event()
            self.activeList[processTag] = (cancel_event, wait_event, outProcessor)
            evkwargs['cancel_event'], evkwargs['wait_event'] = self.activeList[processTag][:2]
            cancel_event.set()
            wait_event.set()
        elif eventType == PROCESS_CANCEL:
            if evkwargs['origen'] == 1: # Procesos cancelados por el sistema
                self.counter = 0
                self.waitingList = []
            self.activeList.pop(processTag)
        else:   # PROCESS_END, PROCESS_CANCEL, PROCESS_ERROR
            self.activeList.pop(processTag)

        okFlag = (eventType == PROCESS_START) or (eventType == PROCESS_END)

        """En la variable toProcess se van a almacenar los indices en los que para 
        su activación se require del proceso en trámite"""
        initialTag = processTag
        toProcess = [initialTag]
        self.preActiveList = []
        while toProcess:
            processTag = toProcess.pop()
            key = '_beg%s_' if eventType == PROCESS_START else '_end%s_'
            key = key % processTag
            relatedToProcessTag = []
            for k, item in enumerate(self.waitingList):
                (startEq, locals), genFunc, args, kwargs = item
                if '"%s"' % processTag in startEq:
                    if not okFlag: relatedToProcessTag.append(k)
                    locals[key] = True
                isReady = eval(startEq, locals)
                if not isReady: continue
                self.preActiveList.append(kwargs['thrTag'])
                if okFlag:
                    relatedToProcessTag.append(k)
                """Los que quedan habilitados con este evento se colocan con 
                ecuación startEq = True"""
                self.waitingList[k] = (("True", locals), genFunc, args, kwargs)
            if not okFlag and relatedToProcessTag:
                """Acá se invierte la lista relatedToProcessTag para sacar de waiting list"""
                relatedToProcessTag = map(self.waitingList.pop, relatedToProcessTag[::-1])
                relatedToProcessTag = map(lambda x: x[-1]['thrTag'], relatedToProcessTag)
                relatedToProcessTag = relatedToProcessTag[::-1]

                eventMessage = 'Falla en proceso %s cancela proceso %s'
                for tag in relatedToProcessTag:
                    message = eventMessage % (initialTag, tag)
                    self.syncQueue.put((PROCESS_MESSAGE, tag, outProcessor, (message,), kwargs))
                toProcess.extend(relatedToProcessTag)

        if not relatedToProcessTag and not self.preActiveList: return
        if relatedToProcessTag:
            k = relatedToProcessTag.pop()
        else:
            thrTag = self.preActiveList[0]
            for k, item in enumerate(self.waitingList):
                kwargs = item[3]
                if thrTag == kwargs['thrTag']: break
            else:
                return
        item = self.waitingList.pop(k)
        eqVars, genFunc, args, kwargs = item
        self.startProcess(genFunc, args, kwargs)

    def loadThread(self, genFunc, args, kwargs, outProcessor=None,
                   processTag=None, startEq=None):
        """
        :param genFunc: generator function
        :param args: args to genFunc
        :param kwargs: kwargs to genFunc
        :param outProcessor: Function to be call on results fron genFunc
        :param processTag: Tag to identify the thread in communicating with
                the owner
        :param startEq: Equation that must be evaluate to true if the
                process must start inmediately (startEq=None) or wait for
                some conditions to be fullfiled.
        :return: None.
        """
        outProcessor = outProcessor or self.processMessage
        kwargs['outProcessor'] = outProcessor
        if processTag is None:
            self.counter += 1
            processTag = '_%s_' % self.counter
        if processTag in self.activeList:
            outProcessor(PROCESS_ERROR, processTag, outProcessor,
                                      Exception('Un proceso con el mismo Id se encuentra activo'),**kwargs)
            return
        kwargs['thrTag'] = processTag
        if startEq:
            locals = self.prepareEqLocals(startEq)
            startEq = startEq.replace(' ', '').replace('*', ' and ').replace('+', ' or ')
            isReady = eval(startEq, locals)
            if not isReady:
                self.waitingList.append(((startEq, locals), genFunc, args, kwargs))
                return
        self.startProcess(genFunc, args, kwargs)

    def startProcess(self, aFunction, args, kwargs):
        processTag, outProcessor = kwargs.pop('thrTag'), kwargs.pop('outProcessor')
        self.mutex.set()
        if not self.syncProcess:
            self.guiOwner.after(100, self.syncWorker, False)
        self.startAsyncThreads()
        self.activeList[processTag] = None
        toQueue = [PROCESS_DATA, processTag, aFunction, args, kwargs, outProcessor]
        self.asyncQueue.put(toQueue)

    def prepareEqLocals(self, startEq):
        pattern = r'[+*]*(?:start|stop)\("(.+?)"\)[*+]*'
        procIds = CustomRegEx.findall(pattern, startEq.replace(' ', ''))
        locals = dict()
        for id in procIds:
            key2, key1 = '_end%s_' % id, '_beg%s_' % id
            locals[key1] = id in self.activeList
            locals[key2] = False

        functions = dict(lt=lambda x, n: self.actProcess(x) < n,
                      gt=lambda x, n: self.actProcess(x) > n,
                      isact= lambda x: x in self.activeList,
                      start=lambda x:locals['_beg%s_'%x],
                      stop=lambda x: locals['_beg%s_'%x] and locals['_end%s_'%x])
        locals.update(functions)
        return locals

    def actProcess(self, grpTag):
        actProc = len([x for x in self.activeList if x.startswith(grpTag)])
        testProc = len([x for x in self.preActiveList if x.startswith(grpTag)])
        return actProc + testProc

    def processMessage(self, *args, **kwargs):
        """
        System Message Listener default.
        :param args: List with the following structure:
                     (messageId,  #  PROCESS_START, PROCESS_END,
                                  #  PROCESS_CANCEL, PROCESS_ERROR,
                                  #  PROCESS_PAUSE, PROCESS_MESSAGE
                     processId,   #  Process identifier, assign at load time-
                     message)     #  Aditional information. When messageId is
                                  #  PROCESS_ERROR it is the object error (Exception)
        :param kwargs: kwargs supply by the user at load time.
        :return: Must be None if the user want the system continue event processing
        as usual. Must return PROCESS_END to ignore the event.
        """
        pass

    def signalProcess(self, processTag=None, event='cancel'):
        """
        Function to cancel all process or signal an processTag process to cancel
        wait or resume
        :param processTag: Process tag, when is None the only event generated is cancel
                    all threads.
        :param event: it can be one of the following values:
                      "cancel": Terminate the process
                      "wait": Pause the process.
                      "resume": Resume a process in the "wait" state.
        :return: None
        """
        if processTag is None:
            self.mutex.clear()
            while not self.asyncQueue.empty():
                self.asyncQueue.get()
                self.asyncQueue.task_done()
            while not self.syncQueue.empty():
                self.syncQueue.get()
                self.syncQueue.task_done()
            toQueue = [PROCESS_MESSAGE, None, None, [], {}, self.processMessage()]
            for k in range(self.activeWorkers):
                self.asyncQueue.put(toQueue)
            return
        elif processTag not in self.activeList:
            raise Exception("%s is not an active process"%processTag)
        cancel_event, wait_event, outProcessor = self.activeList[processTag]
        if event == 'cancel':
            cancel_event.clear()
        elif event == 'wait':
            wait_event.clear()
            args = (PROCESS_PAUSE, processTag,'Proceso pausado')
            kwargs = {}
            outProcessor(*args, **kwargs)

        elif event == 'resume':
            wait_event.set()
            args = (PROCESS_PAUSE, processTag, 'Proceso reanudado')
            kwargs = {}
            outProcessor(*args, **kwargs)
        else:
            cancel_event.clear()


if __name__ == '__main__':
    import inspect
    bvc_url = r'http://www.bvc.com.co/pps/tibco/portalbvc/Home/Mercados/enlinea/acciones'
    tableHead = r'(?#<table id="textTitulos" .tr<th{1.a.*=&Mnemo& 2.*=&Cantidad& 3.a.*=&Volumen& 4.*=&PCierre& 5.a.*=&Variacion&}>*>)'
    tableBody = r'(?#<div id="tbAcNegociadas" .tr<td{1.a.*=&td1& 2.*=&td2& 3.*=&td3& 4.*=&td4& 5.*=&td5&}>*>)'

    thManager = threadManager()
    thManager.loadThread(parsingUrlData, (bvc_url, tableBody), {}, 'processingWebData')
    thManager.startTread(wait=True)
    print 'finalice'
